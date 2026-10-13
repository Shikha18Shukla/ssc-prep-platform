"""Build the reviewed original SSC Speed, Time & Distance question bank."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "speed_time_distance_verified_batch.json"

# Difficulty, stem, verified answer, and worked explanation. The independent
# answer oracle is in tests/test_speed_time_distance_verified_batch.py.
ROWS = [
    # Easy: direct formulas, unit conversions, and single-step applications.
    ("EASY", "A car travels at 54 km/h for 3 hours. How far does it travel?", 162, "Distance = speed × time = 54 × 3 = 162 km."),
    ("EASY", "A bus covers 180 km in 4 hours. What is its average speed?", 45, "Average speed = 180 ÷ 4 = 45 km/h."),
    ("EASY", "How long does a 210 km journey take at a constant speed of 70 km/h?", 3, "Time = distance ÷ speed = 210 ÷ 70 = 3 hours."),
    ("EASY", "Convert 72 km/h into metres per second.", 20, "Multiply by 5/18: 72 × 5/18 = 20 m/s."),
    ("EASY", "Convert 15 m/s into kilometres per hour.", 54, "Multiply by 18/5: 15 × 18/5 = 54 km/h."),
    ("EASY", "A cyclist rides at 48 km/h for 2.5 hours. Find the distance covered.", 120, "Distance = 48 × 2.5 = 120 km."),
    ("EASY", "A runner covers 360 metres in 30 seconds. What is the runner's speed in m/s?", 12, "Speed = 360 ÷ 30 = 12 m/s."),
    ("EASY", "A train travels at 42 km/h for 90 minutes. How many kilometres does it cover?", 63, "90 minutes = 1.5 hours; distance = 42 × 1.5 = 63 km."),
    ("EASY", "A delivery van covers 180 km in 2.5 hours. Find its average speed.", 72, "Average speed = 180 ÷ 2.5 = 72 km/h."),
    ("EASY", "A vehicle covers equal distances at 40 km/h and 60 km/h. What is its average speed for the whole trip?", 48, "For equal distances, average speed = 2uv/(u+v) = 2×40×60/100 = 48 km/h."),
    ("EASY", "A car travels for 30 minutes at 20 km/h and then for 90 minutes at 60 km/h. Find its average speed.", 50, "It covers 10 km and 90 km in 2 hours; the average is 100/2 = 50 km/h."),
    ("EASY", "A bus moves at 45 km/h for 4 hours and is stopped for 30 minutes. What is its average speed over the complete elapsed time?", 40, "It covers 45×4 = 180 km in 4.5 elapsed hours; 180/4.5 = 40 km/h."),
    ("EASY", "A boat moves at 12 km/h in still water. The stream flows at 2 km/h. Find the downstream speed.", 14, "Downstream speed = 12 + 2 = 14 km/h."),
    ("EASY", "A boat's speed in still water is 15 km/h and the current is 3 km/h. Find its upstream speed.", 12, "Upstream speed = 15 − 3 = 12 km/h."),
    ("EASY", "Two cars approach each other at 48 km/h and 36 km/h. What is their relative speed?", 84, "Opposite-direction relative speed is the sum: 48 + 36 = 84 km/h."),
    ("EASY", "A 150 m train passes a pole in 10 seconds. Find its speed in m/s.", 15, "The train covers its own length: 150/10 = 15 m/s."),
    ("EASY", "How long does a 180 m train travelling at 54 km/h take to pass a pole?", 12, "54 km/h = 15 m/s; time = 180/15 = 12 seconds."),
    ("EASY", "A pedestrian walks 1.5 km in 30 minutes. Find the speed in km/h.", 3, "30 minutes is 0.5 hour; 1.5/0.5 = 3 km/h."),
    ("EASY", "A scooter covers 12 km in 40 minutes. What is its speed in km/h?", 18, "40 minutes = 2/3 hour; speed = 12 ÷ (2/3) = 18 km/h."),
    ("EASY", "An athlete runs 300 m in 60 seconds. What is the speed in km/h?", 18, "300/60 = 5 m/s; 5×18/5 = 18 km/h."),
    ("EASY", "At 80 km/h, how long will a truck take to travel 240 km?", 3, "Time = 240/80 = 3 hours."),
    ("EASY", "Convert 5 m/s to km/h.", 18, "5 × 18/5 = 18 km/h."),
    ("EASY", "A car travelling at 60 km/h is 30 km behind a car travelling at 45 km/h in the same direction. How long will it take to catch up?", 2, "Closing speed = 60−45 = 15 km/h; time = 30/15 = 2 hours."),
    ("EASY", "Two towns are 220 km apart. Cars leave them at the same time and travel towards each other at 50 km/h and 60 km/h. When do they meet?", 2, "Combined speed = 110 km/h; meeting time = 220/110 = 2 hours."),
    ("EASY", "In a 100 m race, Arun finishes in 20 seconds and Bala in 25 seconds. By how many metres does Arun beat Bala?", 20, "When Arun finishes, Bala has run 100×20/25 = 80 m; the lead is 20 m."),
    ("EASY", "A 120 m train travels at 72 km/h and crosses a 180 m bridge. How many seconds does it take?", 15, "Total distance is 300 m; 72 km/h = 20 m/s; time = 300/20 = 15 s."),
    ("EASY", "A car travels for one hour at 40 km/h and one hour at 60 km/h. Find its average speed.", 50, "The equal-time average is (40+60)/2 = 50 km/h."),
    ("EASY", "A vehicle travels 90 km at 45 km/h and then another 90 km at 60 km/h. Find the total travel time.", 3.5, "The two legs take 2 hours and 1.5 hours, respectively; total = 3.5 hours."),
    ("EASY", "A ferry covers 60 km downstream in 4 hours. What is its downstream speed?", 15, "Speed = 60/4 = 15 km/h."),
    ("EASY", "A driver covers 20 km at 40 km/h and the remaining 40 km at 80 km/h. Find the average speed for the 60 km trip.", 60, "The times are 0.5 h and 0.5 h; total distance 60 km in 1 h gives 60 km/h."),

    # Medium: combine stages, relative motion, and solve for a missing quantity.
    ("MEDIUM", "A motorist covers the same route once at 75 km/h and once at 50 km/h. Find the average speed over both equal-distance journeys.", 60, "For equal distances, mean speed = 2×75×50/(75+50) = 60 km/h."),
    ("MEDIUM", "A van drives 3 hours at 48 km/h and then 2 hours at 66 km/h. Find its average speed for the 5-hour journey.", 55.2, "Distance = 3×48 + 2×66 = 276 km; 276/5 = 55.2 km/h."),
    ("MEDIUM", "A 360 km route is travelled for 240 km at 60 km/h and for the remaining distance at 40 km/h. Find the average speed for the route.", 360/7, "The two legs take 4 and 3 hours, so the average is 360/7 = 51.43 km/h."),
    ("MEDIUM", "A coach covers 240 km at an average of 48 km/h including a stop. While moving, its speed is 60 km/h. How long was it stopped?", 1, "Elapsed time = 240/48 = 5 h; moving time = 240/60 = 4 h; stop = 1 h."),
    ("MEDIUM", "A driver reaches a destination 20 minutes late at 30 km/h, but would arrive on time at 40 km/h. How far away is the destination?", 40, "The time difference is d/30−d/40 = d/120 hour = 1/3 hour; d = 40 km."),
    ("MEDIUM", "A 72 km/h train passes a pole in 15 seconds. What is the train's length?", 300, "72 km/h = 20 m/s; length = 20×15 = 300 m."),
    ("MEDIUM", "A 200 m train moving at 54 km/h passes a platform. It takes 40 seconds to clear the platform. Find the platform's length.", 400, "54 km/h = 15 m/s; total distance = 15×40 = 600 m; platform = 600−200 = 400 m."),
    ("MEDIUM", "Two trains approach each other at 72 km/h and 54 km/h. What is their relative speed in metres per second?", 35, "Convert and add: (72+54)×5/18 = 35 m/s."),
    ("MEDIUM", "Two trains of lengths 220 m and 180 m travel in the same direction at 72 km/h and 54 km/h. How long does the faster train take to overtake the slower one?", 80, "Relative speed = 18 km/h = 5 m/s; crossing distance = 400 m; time = 400/5 = 80 s."),
    ("MEDIUM", "A boat covers 48 km downstream and 36 km upstream, taking 3 hours for each leg. Find the speed of the current.", 2, "Downstream and upstream speeds are 16 and 12 km/h; current = (16−12)/2 = 2 km/h."),
    ("MEDIUM", "A boat's downstream speed is 22 km/h and its upstream speed is 14 km/h. Find the speed of the stream.", 4, "Current speed is half the difference: (22−14)/2 = 4 km/h."),
    ("MEDIUM", "A boat travels 72 km upstream at 12 km/h and returns downstream at 18 km/h. How much longer does the upstream leg take?", 2, "Upstream takes 6 hours; downstream takes 4 hours; difference = 2 hours."),
    ("MEDIUM", "In a 200 m race, A beats B by 25 m. In a separate 200 m race, B beats C by 20 m. By how many metres does A beat C in a 200 m race?", 42.5, "Speed ratios are A:B=200:175 and B:C=200:180; C covers 200×175/200×180/200 = 157.5 m when A finishes, so the lead is 42.5 m."),
    ("MEDIUM", "Two runners cover a 400 m track at 8 m/s and 6 m/s. How much earlier does the faster runner finish one lap?", 50/3, "Their lap times are 400/8=50 s and 400/6=66⅔ s; the difference is 16⅔ s."),
    ("MEDIUM", "A 120 km trip is scheduled at 40 km/h. After a one-hour delay, what speed is required over the remaining schedule to arrive at the originally planned time?", 60, "The scheduled trip takes 3 h; after losing 1 h, 120 km must be covered in 2 h, requiring 60 km/h."),
    ("MEDIUM", "A taxi travels 30 km at 30 km/h and then 60 km at 60 km/h. Find its average speed over the whole journey.", 45, "Each leg takes 1 hour; 90 km in 2 hours gives 45 km/h."),
    ("MEDIUM", "A journey has one-third of its distance at 30 km/h and the remaining two-thirds at 60 km/h. Find the average speed.", 45, "For distance D, time = D/90 + D/90 = D/45; average speed is 45 km/h."),
    ("MEDIUM", "For a fixed journey, a vehicle takes 24 minutes longer at 48 km/h than at 60 km/h. How long does the slower journey take?", 120, "If the slower time is t, the faster time is (48/60)t; their difference is t/5=24 min, so t=120 min."),
    ("MEDIUM", "A person walks 6 km to a destination at 4 km/h and returns by the same route at 6 km/h. Find the total journey time.", 2.5, "Outward time = 1.5 h and return time = 1 h; total = 2.5 h."),
    ("MEDIUM", "A bus leaves at 40 km/h. A car leaves the same point 45 minutes later at 60 km/h. How far from the start does the car catch the bus?", 90, "The bus has a 30 km lead; relative speed is 20 km/h, so catch-up takes 1.5 h. The car travels 60×1.5 = 90 km."),
    ("MEDIUM", "Two vehicles start 300 km apart and travel towards each other at 40 km/h and 35 km/h. How long until they meet?", 4, "Closing speed = 75 km/h; time = 300/75 = 4 hours."),
    ("MEDIUM", "In a 400 m race, the winner runs at 8 m/s and the runner-up at 7 m/s. By how many metres does the winner finish ahead?", 50, "The race takes the winner 50 s; in that time the runner-up covers 7×50 = 350 m, leaving a 50 m gap."),
    ("MEDIUM", "A train 250 m long travelling at 72 km/h crosses a platform in 27.5 seconds. Find the platform's length.", 300, "Speed = 20 m/s; total distance = 20×27.5 = 550 m; platform = 550−250 = 300 m."),
    ("MEDIUM", "A vehicle travels at 12.5 m/s for 8 minutes. How many kilometres does it cover?", 6, "Eight minutes is 480 seconds; distance = 12.5×480 = 6,000 m = 6 km."),
    ("MEDIUM", "A boat's downstream and upstream speeds are 18 km/h and 14 km/h. Find its speed in still water.", 16, "Still-water speed = (18+14)/2 = 16 km/h."),
    ("MEDIUM", "A motorboat moves at 18 km/h in still water while the stream flows at 4 km/h. How long will it take to travel 88 km downstream?", 4, "Downstream speed = 18+4 = 22 km/h; time = 88/22 = 4 hours."),
    ("MEDIUM", "A cyclist travels for equal periods at 20 km/h and 30 km/h. Find the average speed.", 25, "Equal-time average speed = (20+30)/2 = 25 km/h."),
    ("MEDIUM", "A vehicle's average speed is 45 km/h over a 90 km route, including one stop. It moves at 60 km/h whenever it is moving. Find the stoppage time.", 0.5, "Elapsed time = 90/45 = 2 h; moving time = 90/60 = 1.5 h; stoppage = 0.5 h."),
    ("MEDIUM", "A 210 km trip is planned at 70 km/h. After a 30-minute delay, what average speed is needed to arrive at the planned time?", 84, "Planned duration = 3 h; remaining time = 2.5 h; required speed = 210/2.5 = 84 km/h."),
    ("MEDIUM", "Two cyclists start together at the same point on a 1.2 km circular track and ride in the same direction at 18 km/h and 15 km/h. After how many minutes will the faster cyclist first catch the slower one?", 24, "The faster cyclist gains one lap at 3 km/h; 1.2/3 hour = 0.4 hour = 24 minutes."),

    # Hard: layered timing, train/boat/race reasoning, and multi-stage journeys.
    ("HARD", "A driver travels 2 hours at 60 km/h, stops for 30 minutes, then travels 3 hours at 80 km/h. Find the average speed over the entire elapsed journey.", 720/11, "Distance = 120+240 = 360 km; elapsed time = 5.5 h; average = 360/5.5 = 65.45 km/h."),
    ("HARD", "A car covers one-third of a route at 30 km/h, one-third at 40 km/h and the final third at 60 km/h. Find the average speed for the route.", 40, "For route length D, total time = D/90 + D/120 + D/180 = 3D/40; hence average speed = D/(3D/40) = 40 km/h."),
    ("HARD", "A 60 km journey takes 24 minutes less when driven at 75 km/h instead of 50 km/h. What is the distance?", 60, "The time difference per kilometre is 1/50−1/75 = 1/150 h; a 24-minute difference is 0.4 h, so distance = 60 km."),
    ("HARD", "Town B is 220 km east of Town A. A car leaves A at 40 km/h. One hour later a car leaves B towards A at 50 km/h. How far from A do they meet?", 120, "At the second departure, the first car is 40 km from A, leaving 180 km between them. Closing speed is 90 km/h, so they meet 2 h later; the first car has travelled 120 km."),
    ("HARD", "Two trains of lengths 300 m and 400 m approach each other and cross completely in 20 seconds. One travels at 72 km/h. Find the speed of the other train.", 54, "Combined length is 700 m, so relative speed is 35 m/s = 126 km/h. The other speed is 126−72 = 54 km/h."),
    ("HARD", "A 240 m train travelling at 72 km/h clears a platform in 30 seconds. Find the platform's length.", 360, "The train covers 20×30 = 600 m; subtracting its 240 m length leaves a 360 m platform."),
    ("HARD", "A 300 m train crosses a person walking towards it at 6 km/h in 12 seconds. Find the train's speed in km/h.", 84, "Relative speed = 300/12 = 25 m/s. The pedestrian walks at 6×5/18 = 5/3 m/s, so train speed = 70/3 m/s = 84 km/h."),
    ("HARD", "Two trains of lengths 200 m and 180 m move in the same direction at 72 km/h and 54 km/h. How long do they take to cross each other completely?", 76, "Relative speed = 5 m/s and combined length = 380 m; time = 380/5 = 76 s."),
    ("HARD", "A train passes a pole in 12 seconds and a 300 m bridge in 24 seconds. Find the train's length.", 300, "The bridge adds 300 m and 12 s, so speed is 25 m/s; train length = 25×12 = 300 m."),
    ("HARD", "Two trains of lengths 180 m and 220 m cross in opposite directions in 16 seconds. If the first train travels at 54 km/h, find the speed of the second.", 36, "Relative speed = 400/16 = 25 m/s = 90 km/h. Subtracting 54 gives 36 km/h."),
    ("HARD", "A boat covers 90 km downstream in 3 hours and 90 km upstream in 5 hours. Find its speed in still water.", 24, "The directional speeds are 30 and 18 km/h; still-water speed = (30+18)/2 = 24 km/h."),
    ("HARD", "A boat travels 72 km downstream in 3 hours and 60 km upstream in 5 hours. Find the speed of the current.", 6, "Downstream speed = 24 km/h and upstream speed = 12 km/h; current = (24−12)/2 = 6 km/h."),
    ("HARD", "A boat travels 72 km downstream in 3 hours and the same distance upstream in 4.5 hours. Find its speed in still water.", 20, "Directional speeds are 24 and 16 km/h; their mean, the still-water speed, is 20 km/h."),
    ("HARD", "In a 400 m race, A beats B by 40 m, and B beats C by 30 m. By how many metres does A beat C?", 67, "At A's finish B has run 360 m; at B's finish C has run 370 m. Thus C/A speed = (360/400)(370/400)=333/400, so C covers 333 m and A's lead is 67 m."),
    ("HARD", "Two runners start together on a 600 m circular track and run in opposite directions at 6 m/s and 4 m/s. After how many seconds have they met for the second time?", 120, "Their relative speed is 10 m/s; meetings occur every 600/10 = 60 s, so the second meeting is after 120 s."),
    ("HARD", "A vehicle travels for 2 hours at 40 km/h and then 3 hours at 60 km/h. It rests for 30 minutes. Find the average speed for the entire elapsed time.", 520/11, "Distance = 80+180 = 260 km; elapsed time = 5.5 h; average = 260/5.5 = 520/11 = 47.27 km/h."),
    ("HARD", "A 360 km journey is completed at an average of 60 km/h. The first 120 km are at 40 km/h and the next 120 km at 60 km/h. At what speed must the final 120 km be covered?", 120, "The target time is 360/60 = 6 h. The first two stages take 3+2 = 5 h, leaving 1 h for 120 km."),
    ("HARD", "A 270 km route must be covered in 4.5 hours. A car travels the first 90 km at 45 km/h. What speed is required for the remaining distance to meet the target time?", 72, "Target time is 4.5 h; the first stage takes 2 h. The remaining 180 km in 2.5 h requires 72 km/h."),
    ("HARD", "A 500 m train crosses a 600 m platform in 55 seconds and a pole in 25 seconds. What is its speed in km/h?", 72, "Passing the pole gives speed = 500/25 = 20 m/s = 72 km/h; the platform check is (500+600)/20 = 55 s."),
    ("HARD", "A 180 m train crosses a 200 m train moving towards it in 10 seconds. If the first train travels at 72 km/h, find the speed of the second train.", 64.8, "Combined length 380 m gives relative speed 38 m/s. Subtract 20 m/s to get 18 m/s = 64.8 km/h."),
    ("HARD", "Two towns are 320 km apart. A car leaves one at 40 km/h; 30 minutes later another leaves the other town towards it at 56 km/h. How far from the second town do they meet?", 175, "At the second departure, the first car has covered 20 km, leaving 300 km. Closing speed is 96 km/h, so they meet 25/8 h later; the second car travels 56×25/8 = 175 km."),
    ("HARD", "A car covers two-fifths of a journey at 45 km/h and the rest at 60 km/h. Find its average speed for the complete journey.", 900/17, "For distance D, time = (2D/5)/45 + (3D/5)/60 = 17D/900; average = 900/17 = 52.94 km/h."),
    ("HARD", "A journey takes one hour longer at 48 km/h than at 60 km/h. Find the journey's length.", 240, "For distance d, d/48−d/60 = d/240 = 1 hour; therefore d = 240 km."),
    ("HARD", "A motorboat travels 96 km downstream in 4 hours and 72 km upstream in 6 hours. Find the speed of the stream.", 6, "Downstream speed = 24 km/h and upstream speed = 12 km/h; current = (24−12)/2 = 6 km/h."),
    ("HARD", "A 600 km journey has 40% of its distance covered at 60 km/h, the next 40% at 80 km/h and the rest at 100 km/h. Find the average speed.", 600/(240/60+240/80+120/100), "The stages take 4, 3 and 1.2 hours; total time 8.2 h, so average = 600/8.2 = 73.17 km/h."),
    ("HARD", "Two towns are 400 km apart. A car leaves the first at 60 km/h. One hour later a car leaves the other town towards it at 40 km/h; after one hour that car increases its speed to 60 km/h. How long after the first departure do they meet?", 4, "After the first hour the gap is 340 km. During the next hour they close 60+40=100 km, leaving 240 km; at 60+60=120 km/h this takes 2 h. Total = 4 h."),
    ("HARD", "A 360 km round trip is made over two equal 180 km legs. The outward leg is at 45 km/h and the return leg at 60 km/h. Find the average speed for the round trip.", 360/(180/45+180/60), "The legs take 4 and 3 hours; 360 km in 7 hours gives 360/7 = 51.43 km/h."),
    ("HARD", "A train covers 180 km at 60 km/h, stops for 30 minutes, and then covers another 180 km. What speed is required on the second part for an overall average of 72 km/h, including the stop?", 120, "The target total time is 360/72 = 5 h. The first leg and stop take 3.5 h, leaving 1.5 h; 180/1.5 = 120 km/h."),
    ("HARD", "A car leaves a town at 60 km/h. Two hours later it increases its speed to 80 km/h. A second car leaves the same town one hour after the first at 90 km/h. How long after the second car departs does it catch the first?", 4, "At the second departure, the first car has a 60 km lead. For the next hour, the second car closes 30 km, leaving 30 km. Thereafter it gains 10 km/h and catches up in 3 more hours, for 4 hours total."),
    ("HARD", "A boat travels on a river whose current is 4 km/h. It takes 8 hours to travel 48 km upstream and 80 km downstream. Find the boat's speed in still water.", 16, "If still-water speed is v, then 48/(v−4)+80/(v+4)=8. Multiplying out gives v²−16v=0; the physical solution v>4 is 16 km/h."),
]


def display(value):
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}".rstrip("0").rstrip(".")


def build():
    assert len(ROWS) == 90, f"expected 90 questions, got {len(ROWS)}"
    questions = []
    distractor_patterns = ((.75, 1.25, 1.5), (.8, 1.2, 1.4), (.5, 1.5, 2), (.9, 1.1, 1.3))
    for index, (difficulty, stem, answer, explanation) in enumerate(ROWS):
        # Plausible positive nearby numerical distractors, with a rotating answer slot.
        distractors = [round(answer * factor, 2) for factor in distractor_patterns[index % 4]]
        values = [answer, *distractors]
        options = [display(value) for value in values]
        assert len(set(options)) == 4, (index + 1, options)
        correct_index = index % 4
        options[0], options[correct_index] = options[correct_index], options[0]
        labels = "ABCD"
        questions.append({
            "subject_slug": "maths",
            "subcategory_slug": "arithmetic-maths",
            "chapter_slug": "speed-time-and-distance",
            "question_text": stem,
            "options": dict(zip(labels, options)),
            "correct_option": labels[correct_index],
            "explanation": explanation,
            "difficulty": difficulty,
            "is_pyq": False,
            "pyq_year": None,
            "pyq_exam_name": None,
            "source": "Original SSC-style practice question",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"questions": questions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
