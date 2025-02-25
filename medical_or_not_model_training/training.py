import spacy
from spacy.util import minibatch, compounding
import random
from spacy.training.example import Example


MEDICAL_TEST = [
    "been having this weird pain in my chest it comes and goes but sometimes it gets really sharp. does it happen when you're moving around or even when you're resting. both but mostly when I take deep breaths"
    ,
    "I keep waking up in the middle of the night feeling really hot but I don’t think I have a fever. hmm have you checked your temperature just to be sure. yeah it's normal but I feel sweaty and restless"
    ,
    "my stomach’s been upset for like three days now nothing seems to help. have you been eating anything different or spicy foods. not really just my usual meals but it just won’t settle"
    ,
    "the headaches are getting worse especially when I look at screens for too long. have you noticed any vision changes like blurriness or sensitivity to light. yeah actually bright lights make it worse"
    ,
    "so I started this new medication last week but now I feel super tired all the time. that could be a side effect did your doctor mention anything about fatigue. no but I can barely keep my eyes open during the day"
    ,
    "I keep getting this ringing sound in my ears it’s not loud but it’s really annoying. does it happen all the time or just sometimes. mostly at night when everything is quiet"
    ,
    "every time I eat something heavy I get this burning feeling in my chest. sounds like acid reflux do you get it after lying down too. yeah especially after dinner it takes forever to go away"
    ,
    "lately my hands have been feeling kinda numb and tingly mostly in the morning. have you been sleeping in a weird position or could it be circulation issues. not sure but it’s been happening a lot more often"
    ,
    "I’ve been feeling dizzy when I stand up too quickly like I almost lose my balance. have you been drinking enough water or could it be low blood pressure. maybe dehydration I haven’t been drinking much lately"
    ,
    "there’s this weird rash on my arm it’s red and itchy but I don’t know what caused it. did you change any soaps or lotions recently. nope same ones I’ve always used"
    ,
    "I’ve been coughing a lot but it’s dry no mucus or anything. any sore throat or fever. just a little irritation but no fever"
    ,
    "my knees keep hurting especially when I walk up the stairs. could be joint inflammation have you tried resting or ice. yeah but it only helps for a little while"
    ,
    "I keep getting random muscle twitches mostly in my legs. are you getting enough potassium or magnesium in your diet. not sure I don’t really pay attention to that"
    ,
    "for some reason my heart feels like it’s skipping beats every now and then. do you feel lightheaded or short of breath when it happens. no but it makes me nervous"
    ,
    "been having trouble sleeping no matter how tired I am I just can’t fall asleep. are you drinking caffeine late in the day or stressed about something. a little stressed but nothing too crazy"
    ,
    "I feel like I’m always cold even when everyone else says it’s warm. hmm have you had your thyroid levels checked before. no never should I get a test"
    ,
    "I keep getting nosebleeds randomly even when I’m not blowing my nose. have you been in a really dry environment lately. yeah I just moved somewhere with a lot of AC"
    ,
    "I’ve been feeling super bloated even after small meals. could be digestion issues have you tried probiotics. no but I might give that a shot."
    ,
    "for some reason my vision gets blurry after staring at my phone for too long. could be eye strain do you take breaks. not really I should probably start"
    ,
    "my ankle’s been swollen since yesterday but I didn’t twist it or anything. any pain when you press on it or walk around. a little but nothing too bad"]

NON_MEDICAL_TEST = [
    'did you hear about that new restaurant downtown. yeah I heard their pasta is amazing. we should go this weekend',
    """I finally watched that show you told me about
    oh yeah what’d you think
    honestly I didn’t expect that twist at the end"""
    ,
    """I need a new laptop mine is so slow now
    maybe try upgrading the RAM first
    hmm yeah that might be cheaper than buying a new one
    """
    ,
    """I forgot to do the laundry again now I have nothing to wear
    classic just wear the same thing twice
    yeah but I spilled coffee on my jeans
    """
    ,
    """I lost my keys again I swear they just disappear
    did you check your bag or pockets
    yes like three times I might be losing my mind
    """,
"""so I tried cooking that recipe and it was a disaster
what happened
I mixed up salt and sugar it was so bad""",

"""the bus was so packed this morning I could barely breathe
yeah rush hour is the worst
I think I’ll just start waking up earlier""",

"""I need to start working out but I’m too lazy
same but I always say that and never do it
maybe we should go together for motivation""",

"""I saw the funniest video today let me show you
haha okay but if it’s not funny I’m judging you
trust me you’re gonna laugh so hard""",

"""I can’t believe it’s already February time is flying
I know right it feels like New Year’s was just yesterday
seriously I need to get my life together""",

"""I want to plan a trip but I don’t know where to go
somewhere warm maybe the beach
ooh that sounds perfect""",

"""why do I always forget people’s names right after they tell me
same it’s so embarrassing
I just avoid saying their name and hope they don’t notice""",

"""I just saw a dog wearing sunglasses
haha that’s amazing I need to see that
let me find the picture I took""",

"""I need to stop spending money on coffee every day
yeah but it’s so hard to resist
true but my wallet is suffering""",

"""I swear my phone battery dies faster every day
maybe it’s time for a new one
nah I’ll just keep complaining about it""",

"""I think my neighbor is learning the violin
oh no how bad is it
let’s just say I hope they get better soon""",

"""I just realized I left my headphones at home
oh no now you have to actually listen to the world
exactly it’s a nightmare""",

"""I need to clean my room but I keep procrastinating
same I just pretend the mess doesn’t exist
but then I can’t find anything when I need it""",

"""I love how dogs get so excited over the smallest things
right like you throw a ball and they act like it’s the best day ever
we should all have that energy""",

"""I found an old playlist from high school and wow my music taste was questionable
haha what kind of songs were on it
let’s just say there were a lot of embarrassing boy band songs""",
]

VALIDATE_DATA = [
"""Yes sir.  How are you?  I'm full of the devil, how are you?  (Laughter)  Good to see you again.  Oh good to be here.  So cold weather isn't gonna slow you down huh?  Pardon?  Cold weather's not slowing you down.  Oh no, I'm used to this.  Yeah, how long have you been in Chicago now?  Pardon?  How long have you been a Chicagoan?  All my life.  Okay.  All my life.  No I was born right here in Forest Park.  No kidding, right down the street huh.  Right down the street.  When I came back out of service I moved to Maywood with my wife cause I married her while I was in service and uh we looked around, we lived with my mother-in-law and father-in-law for 3 1/2 years.  We were looking for a place to buy.  So we finally found a place and then we took the two of them with em, they went with us.  Uh-huh.  There was a couple of rooms finished off in the basement in the house we bought.  They were with me for over 20 some years.  Wow.  Was that here in Forest Park?  No Melrose Park.  Okay.  They were living in Maywood and we lived with them for 3 1/2 years.  Melrose Park.  Then when we went to Melrose Park in 1948 and I've been there ever since.  Alright wow.  Oh yeah.  You stayed all within the same area pretty much.  More or less yeah.  Oh my daughter wants me to come to New Mexico so bad.  She's got a great big adobe home in Albuquerque.  Uh-huh.  Four bedrooms, three baths, outdoor diving pool.  Not for you though?  Oh no.  (Laughs).  Because she's got two dogs, four cats and two cockatoos.  Oh my gosh.  They're a pet .  Yeah.  And I can't stand it.  Those damn birds, they scream at the top of their voice.  I don't like that.  I don't either.  I'm not into that.  I like peace and quiet.  So how you feeling overall?  Well, I have two little items I would like to mention.  Sure.  One of them is my throat.  Yeah.  I used to sing a lot and uh lately if, now I'm singing in church too.  Uh-huh.  And uh sometimes when I sing it irritates my throat.  Okay.  I was just wondering if I ought to see a throat specialist.  Are you getting pain when you swallow?  Sometimes without any, without any reason it kind of irritates a little bit.  Um, how long has this been going on?  Oh just recently.  Okay.  Yeah.  So it's been going on for several days in a row or does it come and go kind of?  Oh, well sometimes, no it's longer than a few days uh.  Occasionally I get hoarse and even when I'm talking to my daughter on the phone, she dad, what's the matter with your voice and she notices the irregularity.  Okay.  Right now it's, not, it's not quite the pitch that it usually is.  Um has this been like for, I guess what I'm trying to ask you is this just something kind of coming over or like has it been there for a while now?  No it comes and goes.  Okay, so it's not like uh.  Not like a constant.  I gotcha.  Um any, so no real pain, you're able to swallow food okay for the most part?  Oh no, no, no, uh.  I still have my tonsils I don't know if that's any indication.  Do you have any ear pain?  No.  Okay.  Any headaches with this?  No.  Any fevers or chills?  No.  Any coughing at all?  Occasionally but not too much.  Uh day or night that you're coughing?  Mostly day.  Okay.  Have you had allergies?  Uh, well they treated me for allergies down here but I think it was, I think it was a dust allergy that I got when I was working up cleaning out my attic.  Oh yeah, okay um.  Yeah you had medication for that at this point.  Yeah.  Have you been around anyone who's been sick?  Pardon?  Anybody around has been sick?  No.  Okay.  No.  Alright.  Okay, well let's take a look and kind of see .  Uh, the other thing I was thinking about was tingling feet and legs.  It started recently.  Okay how long ago?  Oh two months.  Which uh, is it both feet?  Both feet.  What part of your feet?  Well right now I can feel a little tingling in the feet.  Sometimes it goes up as high as this.  Okay and is it exactly the same on the other side too?  Both the same.  Any trouble walking?  Well, diabetic, sometimes I have trouble with my balance you know, but uh other than that why uh no I can. diabetic, how long have you had diabetes for?  Oh since 1981.  Yeah since '81.  You're still on uh NPH 17 units?  Uh I make it 18 cause it's easier to hit in the in the needle.  Okay and how have your sugars been at home?  Pardon?  Your blood sugars at home?  Yeah.  How have they been?  Alright.  What numbers are you getting?  Oh, it's usually blood pressure runs anywhere from the 130s to the 150s.  That's a little bit higher than before right?  Pardon?  That's a bit higher than prior.  Yeah a little bit higher.  I'm getting ready to send in for a refill on my hydrochlorothiazide.  I've got about 30 days left.  Lisinopril you sent me.  Yeah.  Uh you also have protein in your urine as well and we had both of those, I know lisinopril is one and there's another medicine that's kind of diabetes management.  Um okay.  You want to have a seat up here for me?  Oh sure.  Uh, , got it.  Can I get you to take your shoes and socks off?  Oh sure.  This helps.  I'm not as limber as I used to be.  You're the most nimble 90-year-old person I've seen.  Huh.  You're the most nimble 90-year-old guy I've seen.  (Laughs).  Oh I come in every couple of months and they clip my toenails for me cause I can't reach them down there.  Yeah.  No falls at home?  Pardon?  You've not been falling or anything?  No, no.  You been taking good care of your feet, diabetic stuff?  Oh yeah, yeah.  I got, what is it Caldesene I put in my shoes for.  Can you feel me touching you here?  Yes, yes, yes.  Okay.  Do you wash your feet every day?  As much as I can yeah.  Do you wear tennis shoes?  Pardon?  You wear shoes all the time?  Oh yeah, yeah, yeah.  Okay.   this looks pretty good.  Where do you have the numbness?  Do you feel ?  Yeah, yeah.  I can feel it in there.  It's.  Both these two sides are the same?  Yeah both sides.  This and this is equal?  Yeah.  Okay.  How far up does it go?  Oh about, about where you've got your thumb.  Right here.  Yeah.  Okay, alright.  I was, I went down to uh Texas in August.  Okay.  My granddaughter graduated from basic training for the Air National Guard.  Oh wow.  And uh I had to fly down to Albuquerque and then we drove down to San Antonio.  Holy cow, that's a long drive.  Oh year it is, 12 hours.  Yeah, Texas is a big state you know.  And uh.  Was it the summer or what?  You noticed.  Isn't it hot down there in August?  Not bad.  San Antonio?  It wasn't bad.  Well I'm used to it.  I was down there for two years during the war.  Oh yeah?  I was in Galveston, between.  Galveston is hot yeah.  I was between Galveston and Houston at Camp Wallace for two years.  Did you like it down there?  Well it was nice.  I had my wife with me for a year.  Deep breath in and out.  Breathe normal.  You want the shirt off?  That's fine.  Almost done.  Alright.  Well that sounds alright.  Yeah.  Let's take a look at your throat, can you say ah?  Ah.  Mmm, not too bad okay.  Did you take your blood pressure medicine today?  Oh yeah.  Okay, your blood pressure is high.  No, oh yeah it is every time I come in.  I got the white coat syndrome.  Oh yeah.  My had it too.  Do you check it at home?  Yes.  What is it at home?  Today I think it was 132/51 if I'm not mistaken.  Do you check it every day?  Every day, every morning at 7 o'clock.  Wow.  Okay.  Do you mind if I check it?  No, no, be my guest.  Do you the sleeve off?  No just higher, .  Whatever you need, you just tell me that's all.  We'll get along fine.  (Laughs).  Just relax your arm.  I should of brought my book along, cause I check my blood sugar every morning too.  I think this morning it was 132.  The only thing on that machine that they gave me to test your blood pressure, the pulse always shows up low.  Does it?  Today it was 41.  Your pulse is lower.  Yeah.  I know that.  It's usually lower than average.  Average yeah.  Uh.  Well if you want to check it, you just get a stop watch or look at a clock and you can compare the two you know.  Well I did, they did that here for me uh.  One of the previous doctors I had was wondering whether I needed a pacemaker or not so they had, uh EKGs, a couple of those and uh then they said well we're gonna send you to the doctor, well they sent me to the head man.  I was fortunate to get the best and uh he looked at the EKGs and he checked me over like you're doing and he said what the hell did they send you in here for?  (Laughs)  He says go home and enjoy your life.  Yeah.  But.  They took the pulse and it was low.  He took it and it was at normal.  Yeah.  So it could have been uh yeah.  User error right?  Yeah, yeah, yeah.  Okay, so let's go with your feet.  I think this is probably diabetic.  Yeah.  Um, you know it's not unexpected having diabetes as long as you have.  Well, I see this  advertising medicine on TV, PAD.  That's different.  Is it?  Yeah.  Oh, oh okay.  I don't think you have that.  No I.  That's different.  I was just wondering, I didn't know.  That's poor blood flow down to your legs and I don't think you got that.  Yeah.  You may have some; you know maybe not the best blood flow.  Right.  Just given that we know you have heart problems.  Yeah.  You've been walking the earth for  .  Yeah.  You've expect that from that but it's not the episode you're describing.  Yeah.  You're describing sounds like the very beginnings of diabetic neuropathy.  Oh.  Which is a complication of diabetes.  Oh okay.  Okay.  Other complications that we see is kidneys and the eyes.  Uh question, I have a stationary bicycle in the basement.  Uh-huh.  I get down there whenever I think of it, I get down there and I get on for about 15 minutes, does that help?  Shouldn't have much affect.  say what did you do get another suit (laughs).  Now you .  Oh yeah.  Alright sir, so the first stop will be the Nurses Station and uh, go right down here to this door and it's on your left side then okay.  Yeah, thank you doctor.  Take care.  Have a great holiday.  Merry Christmas and have a safe New Year.  Alright then I'll see you again in uh.  In three months.  Yeah, it'll be early winter.  Okie doke."""

]


def load_data(path):
    results = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            # print(line)
            results.append(line)
    return results


def predict_prescription_intent(nlp, text):
    doc = nlp(text)
    print("\nAnalyzing:", text)
    print("Prediction scores:")
    for label, score in doc.cats.items():
        print(f"{label}: {score:.3f}")

    predicted_category = max(doc.cats, key=doc.cats.get)
    print(f"Predicted category: {predicted_category}")
    return predicted_category


def train_clinical_classifier(training_data):
    # Initialize spaCy
    nlp = spacy.blank('en')
    textcat = nlp.add_pipe('textcat', last=True)
    textcat.add_label('clinical')
    textcat.add_label('non_clinical')

    # Prepare training examples
    examples = []
    for text, annotations in training_data:
        examples.append(Example.from_dict(nlp.make_doc(text), annotations))

    # Initialize the model
    nlp.initialize(lambda: examples)

    # Training loop
    n_iter = 5
    for epoch in range(n_iter):
        random.shuffle(examples)
        losses = {}

        # Batch training
        batches = minibatch(examples, size=4)
        for batch in batches:
            nlp.update(batch, drop=0.2, losses=losses)

        print(f"Epoch {epoch}, Losses: {losses}")

    return nlp

def train():
    path = 'processed_data/medical/processed_data.txt'
    medical_data = load_data(path)
    path = 'processed_data/non_medical/results.txt'
    non_medical_data = load_data(path)

    # import copy
    # Prepare medical examples
    training_data = []
    # annos = {'cats': {'medical': 1.0, 'non_medical': 0.0}}
    for text in medical_data:
        training_data.append((text, {'cats': {'clinical': 1.0, 'non_clinical': 0.0}}))
    # annos = {'cats': {'medical': 0.0, 'non_medical': 1.0}}
    for text in non_medical_data:
        training_data.append((text, {'cats': {'clinical': 0.0, 'non_clinical': 1.0}}))

    nlp = train_clinical_classifier(training_data)
    nlp.to_disk('trained_model.bin')


def validate():
    import csv
    nlp = spacy.load('./trained_model.bin')
    count = 0
    results = []
    # in data/non_medical/train.csv
    # read csv file
    with open('data/non_medical/validation.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        for row in reader:
            count += 1
            # print(row[0], type(row[0]))
            dialog = row[0][1:-1]
            processed_dialog = []
            for line in dialog.split('\n'):
                line = line.strip()
                line = line[1:-1]
                if line.startswith(' '):
                    line = line[1:]
                processed_dialog.append(line)
            result = ''.join(processed_dialog)
            results.append(result)
    for line in results:
        predict_prescription_intent(nlp, line)


def test():
    nlp = spacy.load('./trained_model.bin')
    print('*** clinical')
    for text in MEDICAL_TEST:
        predict_prescription_intent(nlp, text)
    print('*** non clinical below')
    for text in NON_MEDICAL_TEST:
        predict_prescription_intent(nlp, text)


def validate_VALIDATE():
    nlp = spacy.load('./trained_model.bin')
    for text in VALIDATE_DATA:
        predict_prescription_intent(nlp, text)


if __name__ == '__main__':
    # train()
    # test()
    # validate()
    validate_VALIDATE()