import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const answerSaveReliability = new Rate('answer_save_reliability');
const submissionCorrectness = new Rate('submission_correctness');
const submissionReliability = new Rate('submission_reliability');
const users = open(__ENV.USER_CSV).trim().split(/\r?\n/).filter(Boolean).map((line) => {
  const separator = line.indexOf(',');
  if (separator < 1) throw new Error('Each USER_CSV line must contain email,password.');
  return { email: line.slice(0, separator), password: line.slice(separator + 1) };
});
const vuTokens = new Map();

export const options = {
  scenarios: {
    exam_flow: {
      executor: 'constant-vus',
      vus: Number(__ENV.VUS || 10),
      duration: __ENV.DURATION || '5m',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<1500'],
    answer_save_reliability: ['rate>0.99'],
    submission_reliability: ['rate>0.99'],
    submission_correctness: ['rate>0.99'],
  },
};

export function setup() {
  if (!__ENV.BASE_URL || !__ENV.EXAM_ID || !__ENV.SUBJECT_ID || !__ENV.CHAPTER_ID || !__ENV.USER_CSV) {
    throw new Error('Set BASE_URL, catalog IDs, and USER_CSV for an isolated staging environment.');
  }
  if (users.length < Number(__ENV.VUS || 10)) {
    throw new Error('USER_CSV must contain at least one distinct disposable account per virtual user.');
  }
}

const base = __ENV.BASE_URL.replace(/\/$/, '');
const headers = { 'Content-Type': 'application/json' };
const checkJson = (response, label, predicate) => check(response, { [label]: predicate });

export default function () {
  const identity = users[__VU - 1];
  let token = vuTokens.get(__VU);
  if (!token) {
    const login = http.post(`${base}/api/auth/login`, JSON.stringify(identity), { headers });
    if (!checkJson(login, 'login accepted', (r) => r.status === 200)) return;
    token = login.json('access_token');
    vuTokens.set(__VU, token);
  }
  const auth = { ...headers, Authorization: `Bearer ${token}` };

  checkJson(http.get(`${base}/api/tests/history/me`, { headers: auth }), 'dashboard history loaded', (r) => r.status === 200);
  const selection = {
    exam_id: __ENV.EXAM_ID,
    subject_id: __ENV.SUBJECT_ID,
    subcategory_id: __ENV.SUBCATEGORY_ID || null,
    chapter_id: __ENV.CHAPTER_ID,
    test_type: 'CHAPTER_WISE',
    difficulty: __ENV.DIFFICULTY || 'EASY',
    question_count: 10,
  };
  const started = http.post(`${base}/api/tests`, JSON.stringify(selection), { headers: auth });
  if (!checkJson(started, 'test started', (r) => r.status === 201)) return;
  const attempt = started.json();
  check(attempt.questions, {
    'ten unique questions': (qs) => qs.length === 10
      && new Set(qs.map((q) => q.test_question_id)).size === 10
      && new Set(qs.map((q) => q.question_text)).size === 10,
    'four options per question': (qs) => qs.every((q) => q.options.length === 4),
    'answer key hidden while active': (qs) => qs.every((q) => !('correct_option' in q) && !('explanation' in q)),
  });

  const choices = [];
  for (const question of attempt.questions) {
    const selected = question.options[0].option_key;
    const saved = http.put(
      `${base}/api/tests/${attempt.id}/questions/${question.test_question_id}/answer`,
      JSON.stringify({ selected_option: selected }),
      { headers: auth },
    );
    const ok = check(saved, { 'answer save accepted': (r) => r.status === 200 });
    answerSaveReliability.add(ok);
    choices.push({ id: question.test_question_id, selected });
    sleep(Number(__ENV.THINK_TIME_SECONDS || 3));
  }

  const reloaded = http.get(`${base}/api/tests/${attempt.id}`, { headers: auth });
  const persisted = reloaded.status === 200 && choices.every((choice) =>
    reloaded.json('questions').some((q) => q.test_question_id === choice.id && q.selected_option === choice.selected));
  check(reloaded, { 'saved answers persist after attempt reload': () => persisted });

  const submitted = http.post(`${base}/api/tests/${attempt.id}/submit`, null, { headers: auth });
  const submitOk = check(submitted, { 'test submitted': (r) => r.status === 200 });
  submissionReliability.add(submitOk);
  if (!submitOk) return;

  const review = http.get(`${base}/api/tests/${attempt.id}/result`, { headers: auth });
  const reviewed = review.status === 200 ? review.json() : null;
  const consistent = reviewed && reviewed.review.length === 10
    && reviewed.review.every((q) => q.correct_option && q.explanation)
    && choices.every((choice, index) => reviewed.review[index].selected_option === choice.selected)
    && reviewed.correct_count === reviewed.review.filter((q) => q.is_correct).length
    && reviewed.wrong_count === reviewed.review.filter((q) => q.selected_option && !q.is_correct).length
    && reviewed.unanswered_count === reviewed.review.filter((q) => !q.selected_option).length
    && reviewed.question_count === reviewed.correct_count + reviewed.wrong_count + reviewed.unanswered_count
    && reviewed.score === (reviewed.correct_count * 2) - (reviewed.wrong_count * 0.5);
  check(review, {
    'result includes score and explanations': () => Boolean(consistent && reviewed.score !== null),
    'review scoring matches saved responses': () => Boolean(consistent),
  });
  submissionCorrectness.add(Boolean(consistent));

  const history = http.get(`${base}/api/tests/history/me`, { headers: auth });
  check(history, {
    'completed attempt appears in dashboard history': (r) => r.status === 200
      && r.json('previous_tests').some((item) => item.id === attempt.id),
  });
}
