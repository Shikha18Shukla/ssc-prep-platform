"""Import original SSC-level Science questions to bring each chapter to ten active ordinary items.

Questions are original matching exercises grounded in NCERT science concepts. The script
reconciles live deficits and commits through the shared transactional question importer.
Reruns are idempotent because the importer rejects normalized question-text duplicates.
"""
from __future__ import annotations

import json
import random
import sys
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher

from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.database.session import SessionLocal
from app.services.question_import_service import import_questions

REFERENCE = "Original practice; factual reference: NCERT textbooks, https://ncert.nic.in/textbook.php"
# Each statement is an original concise factual description. Options are matched against
# the named concept, so other statements remain plausible but are unambiguously mismatched.
FACTS = {
"cell": [
("Plasma membrane", "The selectively permeable boundary that regulates movement into and out of a cell."),
("Nucleus", "The cell structure that contains most hereditary material and directs many activities."),
("Mitochondrion", "The organelle where most aerobic cellular respiration releases usable energy."),
("Ribosome", "The cell structure where proteins are assembled from amino acids."),
("Chloroplast", "The plant-cell organelle containing chlorophyll and carrying out photosynthesis."),
("Vacuole", "A membrane-bound compartment that stores substances; the large central one helps plant cells maintain turgidity."),
("Cell wall", "The rigid outer layer of plant cells, composed mainly of cellulose."),
("Cytoplasm", "The cell material between the plasma membrane and nucleus where many reactions occur."),
("Osmosis", "The net movement of water through a selectively permeable membrane from higher to lower water potential."),
("Prokaryotic cell", "A cell whose genetic material is not enclosed within a membrane-bound nucleus."),
],
"digestive-system": [
("Salivary amylase", "An enzyme in saliva that begins the digestion of starch."),
("Oesophagus", "The muscular tube that moves swallowed food to the stomach by peristalsis."),
("Hydrochloric acid in the stomach", "It creates an acidic medium and helps activate pepsin."),
("Pepsin", "A stomach enzyme that digests proteins into smaller peptides."),
("Bile", "A liver secretion that emulsifies fats; it contains no digestive enzyme."),
("Pancreatic juice", "It supplies enzymes that act on carbohydrates, proteins and fats in the small intestine."),
("Small intestine", "The principal site where digestion is completed and nutrients are absorbed."),
("Villi", "Finger-like projections that increase the absorptive surface of the small intestine."),
("Large intestine", "It absorbs much of the remaining water and salts from undigested material."),
("Peristalsis", "Wave-like contractions of the alimentary canal that propel its contents."),
],
"respiratory-system": [
("Nasal cavity", "It filters, warms and moistens incoming air."),
("Trachea", "The air passage supported by C-shaped cartilage rings that help keep it open."),
("Bronchi", "The two main branches that carry air from the trachea into the lungs."),
("Alveoli", "Thin-walled lung sacs where oxygen and carbon dioxide diffuse between air and blood."),
("Diaphragm during inhalation", "Its contraction and flattening increase the volume of the thoracic cavity."),
("Haemoglobin", "The red blood-cell protein that binds and transports most oxygen in blood."),
("Aerobic respiration", "The breakdown of glucose using oxygen, yielding carbon dioxide, water and energy."),
("Breathing", "The physical process of moving air into and out of the lungs."),
("Carbon dioxide transport", "Most carbon dioxide in blood is carried as bicarbonate ions in plasma."),
("Larynx", "The structure containing vocal cords and commonly called the voice box."),
],
"brain-and-nervous-system": [
("Cerebrum", "The brain region involved in thinking, memory and voluntary actions."),
("Cerebellum", "The brain region that helps coordinate muscular movement and maintain balance."),
("Medulla oblongata", "The brainstem region regulating involuntary activities such as breathing and heartbeat."),
("Spinal cord", "It conducts nerve impulses and serves as a centre for many reflex actions."),
("Neuron", "The specialised cell that receives and transmits nerve impulses."),
("Dendrites", "Neuron extensions that usually receive signals and carry them toward the cell body."),
("Axon", "The neuron extension that carries impulses away from the cell body."),
("Reflex arc", "The nerve pathway followed during a reflex action, often through the spinal cord."),
("Synapse", "The junction across which a neuron communicates with another cell using chemical signals or electrical transmission."),
("Hypothalamus", "A brain region that links nervous and endocrine control and helps regulate body temperature."),
],
"excretory-system": [
("Kidney", "The organ that filters blood and forms urine."),
("Nephron", "The structural and functional unit of the kidney."),
("Glomerulus", "A tuft of capillaries where blood filtration begins in a nephron."),
("Bowman's capsule", "The cup-shaped nephron structure that receives filtrate from the glomerulus."),
("Selective reabsorption", "The return of useful substances such as glucose, salts and water from filtrate to blood."),
("Ureter", "The tube that carries urine from a kidney to the urinary bladder."),
("Urinary bladder", "The muscular sac that temporarily stores urine."),
("Urethra", "The passage through which urine leaves the body from the bladder."),
("Dialysis", "A procedure that removes wastes from blood when kidneys cannot perform adequate filtration."),
("Urea", "A nitrogenous waste formed mainly in the liver and excreted by the kidneys."),
],
"nutrition": [
("Autotrophic nutrition", "A mode of nutrition in which organisms make organic food from inorganic raw materials."),
("Chlorophyll", "The green pigment that captures light energy for photosynthesis."),
("Photosynthesis", "The process using light to make carbohydrates from carbon dioxide and water, releasing oxygen."),
("Stomata", "Leaf pores that allow gas exchange and are regulated by guard cells."),
("Root hairs", "Extensions that increase the root surface area for absorbing water and mineral ions."),
("Saprotrophic nutrition", "Obtaining nutrients from dead and decaying organic matter, as in many fungi."),
("Parasitic nutrition", "Obtaining nutrients from a living host, often harming it."),
("Ruminants", "Animals that regurgitate partially digested food and chew it again as cud."),
("Bile salts", "They help emulsify fats in the small intestine."),
("Balanced diet", "A diet providing essential nutrients, fibre and energy in suitable amounts."),
],
"glands": [
("Pituitary gland", "An endocrine gland at the base of the brain that regulates several other endocrine glands."),
("Thyroid gland", "It secretes thyroxine, whose synthesis requires iodine."),
("Pancreatic islets", "They release insulin and glucagon to help regulate blood glucose."),
("Adrenal glands", "They secrete adrenaline, which helps prepare the body for emergency responses."),
("Parathyroid glands", "They secrete parathyroid hormone, which helps regulate blood calcium."),
("Testes", "They produce sperm and secrete the male sex hormone testosterone."),
("Ovaries", "They produce ova and secrete oestrogen and progesterone."),
("Insulin", "A pancreatic hormone that lowers blood glucose by promoting its uptake and storage."),
("Adrenaline", "A hormone that increases heart rate and helps prepare the body for a fight-or-flight response."),
("Endocrine gland", "A ductless gland that releases hormones directly into the blood or surrounding fluid."),
],
"skeleton-system": [
("Adult human skeleton", "It typically consists of 206 bones."),
("Femur", "The longest and strongest bone in the human body, located in the thigh."),
("Patella", "The kneecap, a sesamoid bone embedded in a tendon."),
("Humerus", "The long bone of the upper arm, extending from shoulder to elbow."),
("Rib cage", "It protects the heart and lungs and helps with breathing movements."),
("Vertebral column", "It supports the body and protects the spinal cord."),
("Cranium", "The part of the skull that encloses and protects the brain."),
("Cartilage", "A flexible connective tissue found at joints and in structures such as the nose."),
("Ligament", "A tough connective tissue that connects bone to bone at a joint."),
("Tendon", "A strong connective tissue that attaches muscle to bone."),
],
"reproduction": [
("Pollination", "The transfer of pollen grains from anther to stigma."),
("Fertilisation in flowering plants", "Fusion of a male gamete with the egg cell forms a zygote."),
("Ovary of a flower", "After fertilisation, it generally develops into the fruit."),
("Ovule", "After fertilisation, it develops into a seed."),
("Stamen", "The male reproductive part of a flower, consisting of anther and filament."),
("Pistil", "The female reproductive part of a flower, including stigma, style and ovary."),
("Binary fission", "Asexual reproduction in which one parent cell divides into two daughter cells."),
("Budding in Hydra", "A new individual develops as an outgrowth on the parent and later detaches."),
("Human sperm", "The male gamete, produced in the testes."),
("Human ovum", "The female gamete, released from an ovary during ovulation."),
],
"plant-kingdom": [
("Bryophytes", "Small non-vascular plants that commonly require water for fertilisation."),
("Pteridophytes", "Seedless vascular plants that reproduce by spores, such as ferns."),
("Gymnosperms", "Plants whose seeds are not enclosed within fruits."),
("Angiosperms", "Flowering plants whose seeds are enclosed within fruits."),
("Mosses", "Bryophytes that lack true vascular tissue and true roots."),
("Fern", "A pteridophyte with vascular tissues that reproduces by spores."),
("Pinus", "A coniferous gymnosperm that bears seeds on cone scales."),
("Monocotyledon", "An angiosperm whose embryo typically has one cotyledon."),
("Dicotyledon", "An angiosperm whose embryo typically has two cotyledons."),
("Thallophyta", "A traditional plant group with a simple body not differentiated into true roots, stems and leaves."),
],
"animal-kingdom": [
("Porifera", "A group of simple aquatic animals with pores, including sponges."),
("Cnidaria", "Aquatic animals with stinging cells, including Hydra and jellyfish."),
("Platyhelminthes", "Flatworms with a dorsoventrally flattened body."),
("Annelida", "Segmented worms such as earthworms and leeches."),
("Arthropoda", "The largest animal phylum, characterised by jointed appendages and an exoskeleton."),
("Mollusca", "A diverse animal phylum that includes snails, clams and octopuses."),
("Echinodermata", "A marine animal phylum including starfish, with a water vascular system."),
("Pisces", "Aquatic vertebrates that typically breathe through gills and have fins."),
("Amphibia", "Vertebrates that commonly have aquatic larval stages and can live on land as adults."),
("Mammalia", "Vertebrates characterised by hair and mammary glands that produce milk."),
],
"tissues": [
("Meristematic tissue", "Plant tissue with actively dividing cells responsible for growth."),
("Apical meristem", "It occurs at root and shoot tips and increases plant length."),
("Xylem", "Plant vascular tissue that transports water and minerals, mainly from roots upward."),
("Phloem", "Plant vascular tissue that transports sugars and other organic nutrients."),
("Parenchyma", "A common living plant tissue that often stores food and may photosynthesise."),
("Collenchyma", "Living plant tissue that provides flexible support in growing parts."),
("Sclerenchyma", "Plant tissue with thick, lignified walls that provides mechanical strength."),
("Epithelial tissue", "Animal tissue that covers body surfaces and lines cavities and organs."),
("Muscle tissue", "Animal tissue specialised for contraction and movement."),
("Nervous tissue", "Animal tissue specialised to receive stimuli and conduct impulses."),
],
"matter-and-atom": [
("Atom", "The smallest unit of an element that retains the element's chemical identity."),
("Proton", "A positively charged particle found in an atomic nucleus."),
("Neutron", "An electrically neutral particle found in an atomic nucleus."),
("Electron", "A negatively charged particle found outside the atomic nucleus."),
("Atomic number", "The number of protons in the nucleus of an atom."),
("Mass number", "The total number of protons and neutrons in an atomic nucleus."),
("Isotopes", "Atoms of the same element with the same atomic number but different mass numbers."),
("Molecule", "A group of atoms chemically bonded together that behaves as a unit."),
("Ion", "An atom or group of atoms with a net electrical charge."),
("Law of conservation of mass", "In a chemical reaction, total mass remains constant in a closed system."),
],
"metals-and-non-metals": [
("Copper", "A metal commonly used for electrical wiring because it conducts electricity well."),
("Sodium", "A highly reactive metal stored under kerosene to limit contact with air and water."),
("Mercury", "A metal that is liquid at ordinary room temperature."),
("Bromine", "A non-metal that is liquid at ordinary room temperature."),
("Graphite", "A form of carbon that conducts electricity despite being a non-metal."),
("Malleability", "The property that allows a metal to be beaten into thin sheets."),
("Ductility", "The property that allows a material to be drawn into wires."),
("Metal oxides", "They are generally basic, though some such as aluminium oxide are amphoteric."),
("Ionic compounds", "They conduct electricity when molten or dissolved because their ions can move."),
("Rust", "A hydrated iron oxide formed when iron corrodes in the presence of oxygen and moisture."),
],
"acid-base-and-salt": [
("Acid in aqueous solution", "It produces hydrogen ions, present as hydronium ions in water."),
("Base in aqueous solution", "It produces hydroxide ions in water."),
("pH below 7", "At about 25 °C, this indicates an acidic aqueous solution."),
("Litmus in acid", "Blue litmus turns red in an acidic solution."),
("Phenolphthalein in base", "It turns pink in a basic solution."),
("Neutralisation", "The reaction of an acid with a base generally produces salt and water."),
("Common salt", "Sodium chloride is its chemical name."),
("Baking soda", "Sodium hydrogen carbonate is its chemical name."),
("Washing soda", "Crystalline sodium carbonate decahydrate is commonly called washing soda."),
("Plaster of Paris", "It is calcium sulfate hemihydrate, prepared by heating gypsum."),
],
"carbon-and-its-compound": [
("Catenation", "The ability of carbon atoms to form bonds with one another and make chains or rings."),
("Tetravalency of carbon", "A carbon atom can form four covalent bonds."),
("Saturated hydrocarbon", "It contains only carbon-carbon single bonds."),
("Alkene", "An unsaturated hydrocarbon containing at least one carbon-carbon double bond."),
("Ethanol", "Its functional group is hydroxyl, written as –OH."),
("Ethanoic acid", "Its functional group is carboxyl, written as –COOH."),
("Soap", "Its molecules have a hydrophilic ionic end and a hydrophobic hydrocarbon tail."),
("Combustion of carbon compounds", "Complete combustion in sufficient oxygen produces carbon dioxide and water."),
("Homologous series", "A family of organic compounds with the same functional group and successive members differing by –CH2–."),
("Diamond and graphite", "They are allotropes made entirely of carbon with different structures and properties."),
],
"periodic-table": [
("Modern periodic law", "Element properties are periodic functions of their atomic numbers."),
("Groups", "The vertical columns in the modern periodic table are called groups."),
("Periods", "The horizontal rows in the modern periodic table are called periods."),
("Group 1", "The first group contains the alkali metals, excluding hydrogen from that family label."),
("Group 17", "The halogens occupy this group of the modern periodic table."),
("Group 18", "The noble gases are placed in this group."),
("Period number", "For main-group elements, it indicates the number of occupied electron shells."),
("Across a period", "Atomic size generally decreases from left to right in a period."),
("Down a group", "Atomic size generally increases as additional electron shells are occupied."),
("Mendeleev", "He arranged elements largely by atomic mass and left gaps for undiscovered elements."),
],
"chemical-reaction": [
("Combination reaction", "Two or more reactants combine to form a single product."),
("Decomposition reaction", "A single compound breaks down into two or more simpler substances."),
("Displacement reaction", "A more reactive element displaces a less reactive element from its compound."),
("Double displacement reaction", "Ions are exchanged between two compounds to form new compounds."),
("Oxidation", "In the classical oxygen-based definition, it is the gain of oxygen or loss of hydrogen."),
("Reduction", "In the classical oxygen-based definition, it is the loss of oxygen or gain of hydrogen."),
("Exothermic reaction", "A reaction that releases energy to its surroundings, often as heat."),
("Endothermic reaction", "A reaction that absorbs energy from its surroundings."),
("Rancidity", "Oxidation of fats and oils can cause undesirable taste and smell in food."),
("Balancing a chemical equation", "It ensures the same number of atoms of each element on both sides."),
],
"chemistry-in-every-day-life": [
("Antacid", "A mild base used to neutralise excess stomach acid."),
("Tooth enamel", "It is mainly composed of calcium phosphate mineral and can be damaged by acids."),
("Detergent", "It cleans effectively in hard water because it does not form insoluble scum with calcium ions as soap does."),
("Hard water", "It contains dissolved calcium or magnesium salts that interfere with soap lathering."),
("Food preservatives", "They slow spoilage by inhibiting microbial growth or chemical changes."),
("Antibiotics", "Medicines that act against bacteria; they do not treat viral infections."),
("Vaccine", "It stimulates immune memory to help protect against a specific infectious disease."),
("Bleaching powder", "Calcium oxychloride is commonly used to disinfect drinking water."),
("Activated charcoal", "Its porous surface adsorbs substances and is used in some purification processes."),
("Detergent micelle", "Its hydrophobic interiors help trap oily dirt in water."),
],
"motion-and-force": [
("Distance", "The total length of the path travelled; it is a scalar quantity."),
("Displacement", "The shortest directed change from initial to final position; it is a vector quantity."),
("Speed", "Distance travelled per unit time."),
("Velocity", "Displacement per unit time in a specified direction."),
("Acceleration", "The rate of change of velocity with time."),
("Newton's first law", "An object maintains its state of rest or uniform straight-line motion unless acted on by a net external force."),
("Newton's second law", "The net force equals the rate of change of momentum; for constant mass, F = ma."),
("Newton's third law", "Forces between interacting bodies are equal in magnitude and opposite in direction."),
("Momentum", "The product of an object's mass and velocity."),
("Inertia", "The tendency of a body to resist a change in its state of motion."),
],
"gravitation-work-energy": [
("Universal gravitation", "Every pair of masses attracts with force proportional to their masses and inversely proportional to distance squared."),
("Acceleration due to gravity near Earth", "Its average magnitude is about 9.8 m/s²."),
("Mass", "It measures inertia and remains constant when an object is moved between locations."),
("Weight", "The gravitational force on an object, equal to mass times local gravitational acceleration."),
("Free fall", "Motion under gravity alone, neglecting air resistance."),
("Work", "For a constant force, work is the component of force along displacement multiplied by displacement."),
("Kinetic energy", "The energy of motion, equal to one-half mass times speed squared."),
("Gravitational potential energy", "Near Earth's surface, it is commonly calculated as mass × g × height relative to a reference."),
("Power", "The rate at which work is done or energy is transferred."),
("Law of conservation of energy", "Energy changes form but the total energy of an isolated system remains constant."),
],
"optics-and-human-eye": [
("Law of reflection", "The angle of incidence equals the angle of reflection, measured from the normal."),
("Plane mirror image", "It is virtual, erect and the same size as the object."),
("Concave mirror", "It can form real or virtual images depending on the object's position."),
("Convex mirror", "It always forms a virtual, erect and diminished image of a real object."),
("Convex lens", "It converges parallel rays of light to a principal focus."),
("Concave lens", "It diverges parallel rays and forms a virtual, erect and diminished image of a real object."),
("Myopia", "This vision defect is commonly corrected using a concave lens."),
("Hypermetropia", "This vision defect is commonly corrected using a convex lens."),
("Retina", "The light-sensitive layer of the eye on which an image is formed."),
("Iris", "It controls pupil size and therefore regulates how much light enters the eye."),
],
"sound": [
("Sound in air", "It travels as a longitudinal wave through compressions and rarefactions."),
("Frequency", "The number of complete vibrations per second, measured in hertz."),
("Amplitude", "For a sound wave, greater amplitude is generally perceived as greater loudness."),
("Pitch", "It is primarily associated with the frequency of a sound wave."),
("Human audible range", "A typical young human hears frequencies from about 20 Hz to 20,000 Hz."),
("Ultrasound", "Sound with frequency above 20,000 Hz, beyond typical human hearing."),
("Echo", "A reflected sound heard separately when sufficient time separates it from the original."),
("Sound speed", "In general, sound travels faster in solids than in liquids and gases."),
("Vacuum", "Sound cannot propagate through it because there are no material particles to carry the vibration."),
("Wavelength", "The distance between successive corresponding points, such as adjacent compressions."),
],
"electricity": [
("Electric current", "The rate of flow of electric charge, measured in amperes."),
("Potential difference", "Work done per unit charge between two points, measured in volts."),
("Ohm's law", "At constant physical conditions, current through a conductor is proportional to voltage across it."),
("Resistance", "For an ohmic conductor, it is the ratio of potential difference to current."),
("Resistivity", "A material property relating resistance to conductor length and cross-sectional area."),
("Series circuit", "The same current flows through each component in a single path."),
("Parallel circuit", "Each branch has the same potential difference across it."),
("Electrical power", "It is the rate of electrical energy transfer; for a resistor it can be written P = VI."),
("Joule heating", "The heat produced in a resistor is proportional to I²Rt for constant resistance."),
("Fuse", "A safety device with a low-melting element that breaks a circuit when excessive current flows."),
],
"magnetic-effect-and-heating": [
("Magnetic field lines", "Outside a bar magnet they are conventionally directed from north pole to south pole."),
("Like magnetic poles", "They repel one another."),
("Right-hand thumb rule", "With the thumb pointing along current, curled fingers show the magnetic field direction around a straight conductor."),
("Electromagnet", "A current-carrying coil around a soft iron core can act as a temporary magnet."),
("Solenoid", "A long cylindrical coil produces a magnetic field similar to that of a bar magnet."),
("Electric motor", "It converts electrical energy into mechanical energy using the force on a current-carrying conductor in a magnetic field."),
("Electromagnetic induction", "A changing magnetic field through a circuit can induce an electric current."),
("Electric generator", "It converts mechanical energy into electrical energy by electromagnetic induction."),
("Domestic fuse", "It is connected in series with the live wire so an overcurrent disconnects the appliance."),
("Short circuit", "It occurs when a very low-resistance path causes an abnormally large current."),
],
"physics-revision": [
("SI unit of force", "The newton (N) is the SI unit of force."),
("SI unit of energy", "The joule (J) is the SI unit of energy and work."),
("SI unit of power", "The watt (W) is the SI unit of power."),
("Scalar quantity", "It has magnitude but no direction, as with mass or temperature."),
("Vector quantity", "It has both magnitude and direction, as with displacement or force."),
("Density", "Mass per unit volume."),
("Pressure", "Force acting normally per unit area."),
("Latent heat", "Energy absorbed or released during a change of state without a temperature change."),
("Conduction", "Heat transfer through a material without bulk movement of the material."),
("Refraction", "The change in direction of light as it passes between media because its speed changes."),
],
}


def norm(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())

with SessionLocal() as db:
    rows = db.execute(text("""SELECT c.id,c.name,c.slug,count(q.id) FILTER (WHERE q.is_active AND NOT q.is_pyq) ordinary
      FROM chapters c JOIN subjects s ON s.id=c.subject_id JOIN exams e ON e.id=s.exam_id
      JOIN subcategories sc ON sc.id=c.subcategory_id LEFT JOIN questions q ON q.chapter_id=c.id
      WHERE e.slug='ssc' AND e.is_active AND s.slug='gk-gs' AND s.is_active AND sc.slug='science' AND sc.is_active AND c.is_active
      GROUP BY c.id ORDER BY c.display_order""")).all()
    if len(rows) != 28:
        raise SystemExit(f"Expected 28 active Science chapters, found {len(rows)}")
    deficit = {r.slug: max(0, 10-r.ordinary) for r in rows}
    total = sum(deficit.values())
    print(f"Live chapters={len(rows)}; live deficit={total}")
    if total == 0:
        print("Science ordinary-question minimum already satisfied; nothing to import")
        raise SystemExit(0)
    questions=[]
    existing_texts={r.slug: [norm(v) for v in db.execute(text("SELECT q.question_text FROM questions q WHERE q.chapter_id=:id"), {"id":r.id}).scalars()] for r in rows}
    for r in rows:
        need=deficit[r.slug]
        if not need: continue
        facts=FACTS.get(r.slug)
        if facts is None or len(facts)<need:
            raise SystemExit(f"Insufficient reviewed fact items for {r.name}: need {need}")
        for i,(concept,statement) in enumerate(facts):
            stem=f"Which statement correctly matches the concept '{concept}'?"
            if any(SequenceMatcher(None,norm(stem),old).ratio() >= 0.82 for old in existing_texts[r.slug]):
                continue
            # Alternatives describe related but different concepts and are therefore plausible mismatches.
            distractors=[facts[(i+j)%len(facts)][1] for j in range(1,len(facts))]
            random.Random(f"{r.slug}:{i}").shuffle(distractors)
            choices=[statement,*distractors[:3]]
            random.Random(f"order:{r.slug}:{i}").shuffle(choices)
            correct="ABCD"[choices.index(statement)]
            questions.append({"subject_slug":"gk-gs","subcategory_slug":"science","chapter_slug":r.slug,
                "question_text":stem,"option_a":choices[0],"option_b":choices[1],"option_c":choices[2],"option_d":choices[3],
                "correct_option":correct,"explanation":f"{concept}: {statement} The other options describe different concepts.",
                "difficulty":"EASY" if i%3==0 else "MEDIUM","is_pyq":False,"pyq_year":"","pyq_exam_name":"","source":REFERENCE})
            if sum(1 for q in questions if q['chapter_slug']==r.slug)>=need: break
        if sum(1 for q in questions if q['chapter_slug']==r.slug)<need:
            raise SystemExit(f"Near-duplicate filtering left {r.name} short")
    if len(questions)!=total:
        raise SystemExit(f"Generated {len(questions)} for live deficit {total}")
    payload=json.dumps({"questions":questions},ensure_ascii=False).encode("utf-8")
    preview=import_questions(db,payload,"application/json","science_original_minimum.json",True)
    if preview.aborted or preview.errors or preview.duplicates or preview.would_import != total:
        raise SystemExit(f"Validation failed: {preview.model_dump()}")
    print(f"Validated {preview.would_import} new original questions; committing transaction")
    committed=import_questions(db,payload,"application/json","science_original_minimum.json",False)
    if committed.aborted or committed.imported != total or committed.errors or committed.duplicates:
        raise SystemExit(f"Commit result unexpected: {committed.model_dump()}")
    print(f"Imported={committed.imported}")
