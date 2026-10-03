import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات
def check_user_answer(user_answer, correct_answer):
    """
    دالة موحدة للتحقق من صحة الإجابة بغض النظر عن كونها True/False أو اختيار من متعدد
    تقوم بتوحيد الصيغة (Lower case وتنزع المسافات الزائدة) لتجنب أخطاء المطابقة.
    """
    # إذا كانت الإجابة أسئلة صواب وخطأ (True/False)
    if isinstance(correct_answer, bool) or str(correct_answer).lower() in ['true', 'false']:
        # توحيد إجابة المستخدم والإجابة الصحيحة إلى صيغة نصية بحروف صغيرة
        if isinstance(user_answer, bool):
            user_str = str(user_answer).lower()
        else:
            user_str = str(user_answer).strip().lower()
            
        correct_str = str(correct_answer).strip().lower()
        return user_str == correct_str

    # إذا كانت أسئلة اختيار من متعدد (MCQ)
    else:
        # مقارنة النص بعد إزالة المسافات الزائدة وتوحيد الحروف الكبيرة والصغيرة
        user_str = str(user_answer).strip().lower()
        correct_str = str(correct_answer).strip().lower()
        return user_str == correct_str
QUESTIONS_DB = {

    "مبتدئ": [
           {
            "id": 1,
            "type": "mcq",
            "prompt": "Doctors follow strict .... before operations.",
            "options": ["a) limitation", "b) procedures", "c) potential", "d) variety"],
            "answer": "b) procedures"
        },
        {
            "id": 2,
            "type": "mcq",
            "prompt": "Egypt and most African countries have a strong .... in different fields.",
            "options": ["a) partnership", "b) disorganization", "c) location", "d) limitation"],
            "answer": "a) partnership"
        },
        {
            "id": 3,
            "type": "mcq",
            "prompt": "Hussein's job is .... and gives him a steady income.",
            "options": ["a) hybrid", "b) mutual", "c) rural", "d) stable"],
            "answer": "d) stable"
        },
        {
            "id": 4,
            "type": "mcq",
            "prompt": "In .... areas, farmers grow wheat, rice and vegetables.",
            "options": ["a) urban", "b) mutual", "c) rural", "d) medical"],
            "answer": "c) rural"
        },
        {
            "id": 5,
            "type": "mcq",
            "prompt": "Karim and Aya have .... respect for each other.",
            "options": ["a) hybrid", "b) mutual", "c) rural", "d) single"],
            "answer": "b) mutual"
        },
        {
            "id": 6,
            "type": "mcq",
            "prompt": "My factory produces high-quality .... for clothes.",
            "options": ["a) commitment", "b) funding", "c) infrastructure", "d) textile"],
            "answer": "d) textile"
        },
        {
            "id": 7,
            "type": "mcq",
            "prompt": "Our company will .... its business to Africa next year.",
            "options": ["a) expand", "b) manufacture", "c) boost", "d) demonstrate"],
            "answer": "a) expand"
        },
        {
            "id": 8,
            "type": "mcq",
            "prompt": "The airport is the main .... to the capital city.",
            "options": ["a) cooperation", "b) conference", "c) stability", "d) gateway"],
            "answer": "d) gateway"
        },
        {
            "id": 9,
            "type": "mcq",
            "prompt": "The charity collected .... to build a new hospital.",
            "options": ["a) commitment", "b) funding", "c) infrastructure", "d) textile"],
            "answer": "b) funding"
        },
        {
            "id": 10,
            "type": "mcq",
            "prompt": "The company plans to .... their production next year.",
            "options": ["a) address", "b) stand out", "c) scale down", "d) double"],
            "answer": "d) double"
        },
        {
            "id": 11,
            "type": "mcq",
            "prompt": "The current plan aims at better .... of technology in schools.",
            "options": ["a) integration", "b) summit", "c) scholarship", "d) conference"],
            "answer": "a) integration"
        },
        {
            "id": 12,
            "type": "mcq",
            "prompt": "The leaders met to improve .... between their countries.",
            "options": ["a) textile", "b) gateway", "c) cooperation", "d) conference"],
            "answer": "c) cooperation"
        },
        {
            "id": 13,
            "type": "mcq",
            "prompt": "The main .... of this project is the lack of funding.",
            "options": ["a) limitation", "b) procedure", "c) potential", "d) variety"],
            "answer": "a) limitation"
        },
        {
            "id": 14,
            "type": "mcq",
            "prompt": "The monorail is part of Egypt's modern .... .",
            "options": ["a) cooperation", "b) funding", "c) infrastructure", "d) textile"],
            "answer": "c) infrastructure"
        },
        {
            "id": 15,
            "type": "mcq",
            "prompt": "Africa is a large .... with many countries.",
            "options": ["a) continent", "b) material", "c) scholarship", "d) enterprise"],
            "answer": "a) continent"
        },
        {
            "id": 16,
            "type": "mcq",
            "prompt": "Ahmed started a small business .... of his own in his town.",
            "options": ["a) partnership", "b) development", "c) enterprise", "d) initiative"],
            "answer": "c) enterprise"
        },
        {
            "id": 17,
            "type": "mcq",
            "prompt": "Ali has a/an .... dream of becoming a pilot.",
            "options": ["a) sustainable", "b) impressed", "c) uncommon", "d) ambitious"],
            "answer": "d) ambitious"
        },
        {
            "id": 18,
            "type": "mcq",
            "prompt": "Aya has gained enough teaching .... from her summer job.",
            "options": ["a) attention", "b) collaboration", "c) experience", "d) location"],
            "answer": "c) experience"
        },
        {
            "id": 19,
            "type": "mcq",
            "prompt": "Egypt launched a national .... to save water.",
            "options": ["a) textile", "b) development", "c) trade", "d) initiative"],
            "answer": "d) initiative"
        },
        {
            "id": 20,
            "type": "mcq",
            "prompt": "Egypt sells oranges and, .... , buys tea.",
            "options": ["a) to return", "b) in return", "c) as a train", "d) in advance"],
            "answer": "b) in return"
        },
        {
            "id": 21,
            "type": "mcq",
            "prompt": "Egypt will .... more oranges to Europe this year.",
            "options": ["a) import", "b) export", "c) invest", "d) expand"],
            "answer": "b) export"
        },
        {
            "id": 22,
            "type": "mcq",
            "prompt": "Egypt .... some products from several countries.",
            "options": ["a) exports", "b) imports", "c) attends", "d) shapes"],
            "answer": "b) imports"
        },
        {
            "id": 23,
            "type": "mcq",
            "prompt": "Experience helps farmers start .... businesses.",
            "options": ["a) agricultural", "b) raw", "c) uncommon", "d) urban"],
            "answer": "a) agricultural"
        },
        {
            "id": 24,
            "type": "mcq",
            "prompt": "Farmers in the Sudan can grow crops thanks to the availability of water.",
            "options": ["a) life-changing", "b) solar-powered", "c) small-scale", "d) year-round"],
            "answer": "d) year-round"
        },
        {
            "id": 25,
            "type": "mcq",
            "prompt": "Farmers need .... crops that can survive harsh weather.",
            "options": ["a) drought-tolerating", "b) community-driven", "c) climate-resilient", "d) tremendous-looking"],
            "answer": "c) climate-resilient"
        },
        {
            "id": 26,
            "type": "mcq",
            "prompt": "It rained .... during the night.",
            "options": ["a) heavily", "b) mutually", "c) jointly", "d) rurally"],
            "answer": "a) heavily"
        },
        {
            "id": 27,
            "type": "mcq",
            "prompt": "Knowing two languages is .... in today's world.",
            "options": ["a) environmental", "b) advantageous", "c) joint", "d) raw"],
            "answer": "b) advantageous"
        },
        {
            "id": 28,
            "type": "mcq",
            "prompt": "My grandfather worked as a teacher in Saudi Arabia for a .... .",
            "options": ["a) decade", "b) textile", "c) funding", "d) solution"],
            "answer": "a) decade"
        },
        {
            "id": 29,
            "type": "mcq",
            "prompt": "Nadeen attended a medical .... in Cairo.",
            "options": ["a) cooperation", "b) gateway", "c) stability", "d) conference"],
            "answer": "d) conference"
        },
        {
            "id": 30,
            "type": "mcq",
            "prompt": "Omar likes to .... by wearing formal clothes most of the time.",
            "options": ["a) double", "b) stand out", "c) scale up", "d) address"],
            "answer": "b) stand out"
        },
        {
            "id": 31,
            "type": "mcq",
            "prompt": "Our .... efforts helped us solve the problem.",
            "options": ["a) administrative", "b) disadvantageous", "c) joint", "d) raw"],
            "answer": "c) joint"
        },
        {
            "id": 32,
            "type": "mcq",
            "prompt": "Salma has great .... to become a scientist.",
            "options": ["a) limitation", "b) procedure", "c) potential", "d) variety"],
            "answer": "c) potential"
        },
        {
            "id": 33,
            "type": "mcq",
            "prompt": "Sama will .... the science fair tomorrow.",
            "options": ["a) attend", "b) borrow", "c) flourish", "d) invest"],
            "answer": "a) attend"
        },
        {
            "id": 34,
            "type": "mcq",
            "prompt": "Small shops can .... if they get more support.",
            "options": ["a) attend", "b) exchange", "c) flourish", "d) invent"],
            "answer": "c) flourish"
        },
        {
            "id": 35,
            "type": "mcq",
            "prompt": "Students will .... from free online courses.",
            "options": ["a) attend", "b) benefit", "c) flourish", "d) invest"],
            "answer": "b) benefit"
        },
        {
            "id": 36,
            "type": "mcq",
            "prompt": "Teachers and parents together can .... students' chances of success.",
            "options": ["a) expect", "b) manufacture", "c) boost", "d) demonstrate"],
            "answer": "c) boost"
        },
        {
            "id": 37,
            "type": "mcq",
            "prompt": "The .... class joined the trip to Aswan.",
            "options": ["a) entire", "b) raw", "c) hybrid", "d) environmental"],
            "answer": "a) entire"
        },
        {
            "id": 38,
            "type": "mcq",
            "prompt": "The actor gave a/an .... performance on stage.",
            "options": ["a) sustainable", "b) impressive", "c) common", "d) ambitious"],
            "answer": "b) impressive"
        },
        {
            "id": 39,
            "type": "mcq",
            "prompt": "The channel .... to the climate meeting keeps us informed with latest developments.",
            "options": ["a) entrepreneur", "b) moderator", "c) delegate", "d) innovator"],
            "answer": "b) moderator"
        },
        {
            "id": 40,
            "type": "mcq",
            "prompt": "The city has seen impressive economic .... in recent years.",
            "options": ["a) growth", "b) limitation", "c) irrigation", "d) scale"],
            "answer": "a) growth"
        },
        {
            "id": 41,
            "type": "mcq",
            "prompt": "The factory plans to .... production of solar panels.",
            "options": ["a) stand in", "b) stand out", "c) scale up", "d) address"],
            "answer": "c) scale up"
        },
        {
            "id": 42,
            "type": "mcq",
            "prompt": "The farm uses modern .... systems for watering.",
            "options": ["a) irrigation", "b) textiles", "c) goods", "d) enterprises"],
            "answer": "a) irrigation"
        },
        {
            "id": 43,
            "type": "mcq",
            "prompt": "The New Capital project will .... investors from abroad.",
            "options": ["a) attend", "b) expire", "c) attract", "d) demonstrate"],
            "answer": "c) attract"
        },
        {
            "id": 44,
            "type": "mcq",
            "prompt": "The new museum is a .... building in Giza.",
            "options": ["a) climate-resilient", "b) community-driven", "c) drought-tolerant", "d) tremendous-looking"],
            "answer": "a) climate-resilient"
        },
        {
            "id": 45,
            "type": "mcq",
            "prompt": "The new road project is part of the city's .... plan.",
            "options": ["a) partnership", "b) development", "c) enterprise", "d) summit"],
            "answer": "b) development"
        },
        {
            "id": 46,
            "type": "mcq",
            "prompt": "The new .... connects the village to the train station.",
            "options": ["a) bridge", "b) region", "c) textile", "d) initiative"],
            "answer": "a) bridge"
        },
        {
            "id": 47,
            "type": "mcq",
            "prompt": "The project is ....; it is supported by local people.",
            "options": ["a) climate-resilient", "b) community-driven", "c) tremendous-looking", "d) drought-tolerant"],
            "answer": "b) community-driven"
        },
        {
            "id": 48,
            "type": "mcq",
            "prompt": "The project succeeded because of good .... between the teams.",
            "options": ["a) isolation", "b) collaboration", "c) changing", "d) location"],
            "answer": "b) collaboration"
        },
        {
            "id": 49,
            "type": "mcq",
            "prompt": "The shop sells a wide .... of fresh fruits.",
            "options": ["a) limitation", "b) procedure", "c) potential", "d) variety"],
            "answer": "d) variety"
        },
        {
            "id": 50,
            "type": "mcq",
            "prompt": "The speech caught everyone's .... .",
            "options": ["a) attention", "b) collaboration", "c) experience", "d) location"],
            "answer": "a) attention"
        },
        {
            "id": 51,
            "type": "mcq",
            "prompt": "The teacher will .... the problem of the class in tomorrow's meeting.",
            "options": ["a) double", "b) stand out", "c) scale up", "d) address"],
            "answer": "d) address"
        },
        {
            "id": 52,
            "type": "mcq",
            "prompt": "The village uses a .... pump to get clean water without causing pollution.",
            "options": ["a) year-round", "b) solar-powered", "c) small-scale", "d) life-changing"],
            "answer": "b) solar-powered"
        },
        {
            "id": 53,
            "type": "mcq",
            "prompt": "The World Cup is the biggest football .... .",
            "options": ["a) event", "b) solution", "c) gateway", "d) enterprise"],
            "answer": "a) event"
        },
        {
            "id": 54,
            "type": "mcq",
            "prompt": "This shop sells leather .... like shoes and bags.",
            "options": ["a) goods", "b) textiles", "c) solutions", "d) problems"],
            "answer": "a) goods"
        },
        {
            "id": 55,
            "type": "mcq",
            "prompt": "Walid wants to .... his money in a new business.",
            "options": ["a) attend", "b) benefit", "c) flourish", "d) invest"],
            "answer": "d) invest"
        },
        {
            "id": 56,
            "type": "mcq",
            "prompt": "Winning the scholarship was really a .... event for Yara.",
            "options": ["a) year-round", "b) solar-powered", "c) small-scale", "d) life-changing"],
            "answer": "d) life-changing"
        },
        {
            "id": 57,
            "type": "mcq",
            "prompt": "Zeina will .... her old tablet for a new one.",
            "options": ["a) promote", "b) serve", "c) participate", "d) exchange"],
            "answer": "d) exchange"
        },
        {
            "id": 58,
            "type": "mcq",
            "prompt": "Zeinab started a .... business selling handmade bags for a low price.",
            "options": ["a) yearly-round", "b) solar-powered", "c) small-scale", "d) life-changed"],
            "answer": "c) small-scale"
        },
        {
            "id": 59,
            "type": "mcq",
            "prompt": ".... is the state of being steady and not subject to sudden change or collapse.",
            "options": ["a) Limitation", "b) Stability", "c) Recommendation", "d) Scholarship"],
            "answer": "b) Stability"
        },
        {
            "id": 60,
            "type": "mcq",
            "prompt": "A .... is a type of cloth or woven fabric.",
            "options": ["a) textile", "b) product", "c) loom", "d) metal"],
            "answer": "a) textile"
        },
        {
            "id": 61,
            "type": "mcq",
            "prompt": "A .... is an arrangement where two or more parties cooperate to advance their interests.",
            "options": ["a) Partnership", "b) Scholarship", "c) Commitment", "d) Event"],
            "answer": "a) Partnership"
        },
        {
            "id": 62,
            "type": "mcq",
            "prompt": ".... is the process of bringing different groups or systems together to work as one.",
            "options": ["a) Partnership", "b) Integration", "c) Recommendation", "d) Initiative"],
            "answer": "b) Integration"
        },
        {
            "id": 63,
            "type": "mcq",
            "prompt": "A/An .... is a mix of two different things, especially to make something better.",
            "options": ["a) hybrid", "b) initiative", "c) enterprise", "d) summit"],
            "answer": "a) hybrid"
        },
        {
            "id": 64,
            "type": "mcq",
            "prompt": "A .... is a point of entry or access to something larger.",
            "options": ["a) gateway", "b) region", "c) continent", "d) bridge"],
            "answer": "a) gateway"
        },
        {
            "id": 65,
            "type": "mcq",
            "prompt": "Money that is provided to support a project or activity is called .... .",
            "options": ["a) goods", "b) funding", "c) textile", "d) material"],
            "answer": "b) funding"
        },
        {
            "id": 66,
            "type": "mcq",
            "prompt": ".... means places in the countryside, away from big cities.",
            "options": ["a) Rural", "b) Administrative", "c) Joint", "d) Strategic"],
            "answer": "a) Rural"
        },
        {
            "id": 67,
            "type": "mcq",
            "prompt": "Something .... is experienced or done by each of two or more parties toward the other.",
            "options": ["a) mutual", "b) sustainable", "c) advantageous", "d) common"],
            "answer": "a) mutual"
        },
        {
            "id": 68,
            "type": "mcq",
            "prompt": "Something .... is made or produced on a large-scale using machinery.",
            "options": ["a) textile", "b) rural", "c) manufactured", "d) raw"],
            "answer": "c) manufactured"
        },
        {
            "id": 69,
            "type": "mcq",
            "prompt": "Something .... is not changing too much, strong and steady.",
            "options": ["a) textile", "b) stable", "c) mutual", "d) economic"],
            "answer": "b) stable"
        },
        {
            "id": 70,
            "type": "mcq",
            "prompt": "The .... is the basic physical and organizational structures and facilities needed for the operation of society.",
            "options": ["a) infrastructure", "b) modernization", "c) irrigation", "d) enterprise"],
            "answer": "a) infrastructure"
        },

        # --- ثانياً: أسئلة الصواب والخطأ (True or False) مصاغة بدقة من معاني وكلمات الملف ---
        {
            "id": 71,
            "type": "tf",
            "prompt": "Stability refers to the state of being steady and not subject to sudden change or collapse.",
            "answer": True
        },
        {
            "id": 72,
            "type": "tf",
            "prompt": "A textile is defined as a type of cloth or woven fabric.",
            "answer": True
        },
        {
            "id": 73,
            "type": "tf",
            "prompt": "Partnership means an arrangement where two or more parties cooperate to advance their interests.",
            "answer": True
        },
        {
            "id": 74,
            "type": "tf",
            "prompt": "Integration is the process of separating different groups or systems so they work alone.",
            "answer": False
        },
        {
            "id": 75,
            "type": "tf",
            "prompt": "A hybrid is a mix of two different things, especially to make something better.",
            "answer": True
        },
        {
            "id": 76,
            "type": "tf",
            "prompt": "A gateway serves as a point of entry or access to something larger.",
            "answer": True
        },
        {
            "id": 77,
            "type": "tf",
            "prompt": "Funding refers to money that is provided to support a project or activity.",
            "answer": True
        },
        {
            "id": 78,
            "type": "tf",
            "prompt": "Rural areas refer to places located inside big bustling metropolitan cities.",
            "answer": False
        },
        {
            "id": 79,
            "type": "tf",
            "prompt": "Mutual respect means that respect is experienced or done by each party toward the other.",
            "answer": True
        },
        {
            "id": 80,
            "type": "tf",
            "prompt": "Manufactured goods are produced on a large-scale using machinery.",
            "answer": True
        },
        {
            "id": 81,
            "type": "tf",
            "prompt": "The infrastructure includes the basic physical and organizational structures needed for society.",
            "answer": True
        },
        {
            "id": 82,
            "type": "tf",
            "prompt": "To expand means to become or make larger or more extensive.",
            "answer": True
        },
        {
            "id": 83,
            "type": "tf",
            "prompt": "Exporting means bringing goods or services into a country from abroad.",
            "answer": False
        },
        {
            "id": 84,
            "type": "tf",
            "prompt": "Importing means bringing goods or services into a country from abroad.",
            "answer": True
        },
        {
            "id": 85,
            "type": "tf",
            "prompt": "A decade is a period of one hundred years.",
            "answer": False
        },
        {
            "id": 86,
            "type": "tf",
            "prompt": "An initiative is a new plan or process to achieve a goal or solve a problem.",
            "answer": True
        },
        {
            "id": 87,
            "type": "tf",
            "prompt": "Climate-resilient crops can survive harsh and changing weather conditions.",
            "answer": True
        },
        {
            "id": 88,
            "type": "tf",
            "prompt": "Solar-powered equipment relies on electricity generated from burning fossil fuels.",
            "answer": False
        },
        {
            "id": 89,
            "type": "tf",
            "prompt": "A small-scale business operates on a limited scale with smaller resources and local reach.",
            "answer": True
        },
        {
            "id": 90,
            "type": "tf",
            "prompt": "Life-changing events have a massive and permanent impact on a person's life.",
            "answer": True
        },
        {
            "id": 91,
            "type": "tf",
            "prompt": "To scale up means to reduce or decrease the size or production of something.",
            "answer": False
        },
        {
            "id": 92,
            "type": "tf",
            "prompt": "To scale back means to decrease or reduce the scale or quantity of something.",
            "answer": True
        },
        {
            "id": 93,
            "type": "tf",
            "prompt": "Cooperation means working together towards a common goal or shared interest.",
            "answer": True
        },
        {
            "id": 94,
            "type": "tf",
            "prompt": "An enterprise is a business or company started by an individual or a group.",
            "answer": True
        },
        {
            "id": 95,
            "type": "tf",
            "prompt": "Irrigation refers to the artificial watering of land to help crops grow.",
            "answer": True
        },
        {
            "id": 96,
            "type": "tf",
            "prompt": "A summit is a high-level meeting or conference between leaders of countries.",
            "answer": True
        },
        {
            "id": 97,
            "type": "tf",
            "prompt": "Advantageous means resulting in good outcomes, helpful, or favorable.",
            "answer": True
        },
        {
            "id": 98,
            "type": "tf",
            "prompt": "A conference is a small private chat between two friends in a cafe.",
            "answer": False
        },
        {
            "id": 99,
            "type": "tf",
            "prompt": "A bridge physically connects two separated places or areas together.",
            "answer": True
        },
        {
            "id": 100,
            "type": "tf",
            "prompt": "To flourish means to grow or develop in a healthy or successful way.",
            "answer": True
        }
    ],
      
    "متوسط": [
              {
            "id": 1,
            "type": "mcq",
            "prompt": "The government is trying to .... the local industry by offering tax reductions and modern equipment.",
            "options": ["a) limit", "b) boost", "c) isolate", "d) disconnect"],
            "answer": "b) boost"
        },
        {
            "id": 2,
            "type": "mcq",
            "prompt": "When the company faced a sudden drop in sales, management decided to .... operations rather than expand.",
            "options": ["a) scale up", "b) scale back", "c) stand out", "d) double"],
            "answer": "b) scale back"
        },
        {
            "id": 3,
            "type": "mcq",
            "prompt": "The success of the new agricultural initiative relies heavily on introducing .... crops that can withstand extreme heat and water scarcity.",
            "options": ["a) climate-resilient", "b) tremendous-looking", "c) small-scale", "d) short-term"],
            "answer": "a) climate-resilient"
        },
        {
            "id": 4,
            "type": "mcq",
            "prompt": "Instead of relying on diesel generators, the remote village installed .... pumps to secure a clean and sustainable water supply.",
            "options": ["a) solar-powered", "b) fossil-fueled", "c) urban-based", "d) factory-made"],
            "answer": "a) solar-powered"
        },
        {
            "id": 5,
            "type": "mcq",
            "prompt": "Winning the full scholarship to study abroad was a .... turning point in her academic career.",
            "options": ["a) life-changing", "b) routine", "c) temporary", "d) standard"],
            "answer": "a) life-changing"
        },
        {
            "id": 6,
            "type": "mcq",
            "prompt": "To remain competitive in the global market, the factory invested heavily in modernizing its underlying .... like transport and energy grids.",
            "options": ["a) infrastructure", "b) limitation", "c) textile", "d) funding"],
            "answer": "a) infrastructure"
        },
        {
            "id": 7,
            "type": "mcq",
            "prompt": "The diplomatic meeting aimed at establishing a strong .... between the two nations to handle economic challenges together.",
            "options": ["a) partnership", "b) division", "c) isolation", "d) barrier"],
            "answer": "a) partnership"
        },
        {
            "id": 8,
            "type": "mcq",
            "prompt": "Successful digital transformation requires the seamless .... of AI tools into daily classroom teaching.",
            "options": ["a) integration", "b) separation", "c) limitation", "d) withdrawal"],
            "answer": "a) integration"
        },
        {
            "id": 9,
            "type": "mcq",
            "prompt": "By adopting strict safety protocols and regular maintenance, the plant ensured long-term operational .... and avoided unexpected breakdowns.",
            "options": ["a) stability", "b) chaos", "c) fluctuation", "d) disruption"],
            "answer": "a) stability"
        },
        {
            "id": 10,
            "type": "mcq",
            "prompt": "The historical port city acts as the main .... for trade routes coming from the southern continent.",
            "options": ["a) gateway", "b) boundary", "c) exit", "d) hurdle"],
            "answer": "a) gateway"
        },
        {
            "id": 11,
            "type": "mcq",
            "prompt": "Local artisans specialize in producing high-end traditional .... crafted from pure Egyptian cotton.",
            "options": ["a) textiles", "b) minerals", "c) metals", "d) plastics"],
            "answer": "a) textiles"
        },
        {
            "id": 12,
            "type": "mcq",
            "prompt": "Securing sufficient venture .... is the primary challenge for startup founders launching tech enterprises.",
            "options": ["a) funding", "b) spending", "c) debt", "d) loss"],
            "answer": "a) funding"
        },
        {
            "id": 13,
            "type": "mcq",
            "prompt": "Unlike hectic metropolitan districts, life in .... communities tends to focus heavily on agriculture and local trade.",
            "options": ["a) rural", "b) urban", "c) industrial", "d) metropolitan"],
            "answer": "a) rural"
        },
        {
            "id": 14,
            "type": "mcq",
            "prompt": "A successful business negotiation must be built on .... trust and clear benefits for all participating sides.",
            "options": ["a) mutual", "b) one-sided", "c) isolated", "d) doubtful"],
            "answer": "a) mutual"
        },
        {
            "id": 15,
            "type": "mcq",
            "prompt": "The company decided to .... its manufacturing capacity by opening three new regional branches next quarter.",
            "options": ["a) expand", "b) shrink", "c) downsize", "d) restrict"],
            "answer": "a) expand"
        },
        {
            "id": 16,
            "type": "mcq",
            "prompt": "Surviving the harsh desert climate requires innovative irrigation techniques and careful resource .... .",
            "options": ["a) management", "b) waste", "c) neglect", "d) depletion"],
            "answer": "a) management"
        },
        {
            "id": 17,
            "type": "mcq",
            "prompt": "The keynote speaker managed to .... the audience's deep interest by sharing groundbreaking research data.",
            "options": ["a) attract", "b) repel", "c) dismiss", "d) ignore"],
            "answer": "a) attract"
        },
        {
            "id": 18,
            "type": "mcq",
            "prompt": "Because of strict budget allocations, the research team had to work within a specific financial .... .",
            "options": ["a) limitation", "b) expansion", "c) surplus", "d) abundance"],
            "answer": "a) limitation"
        },
        {
            "id": 19,
            "type": "mcq",
            "prompt": "Surgeons must strictly follow clinical .... to guarantee patient safety during complex operations.",
            "options": ["a) procedures", "b) guesses", "c) shortcuts", "d) randoms"],
            "answer": "a) procedures"
        },
        {
            "id": 20,
            "type": "mcq",
            "prompt": "The newly elected council launched a national .... to encourage youth entrepreneurship.",
            "options": ["a) initiative", "b) obstacle", "c) barrier", "d) restriction"],
            "answer": "a) initiative"
        },
        {
            "id": 21,
            "type": "mcq",
            "prompt": "The country relies on raw material exports, while it heavily .... technological equipment from abroad.",
            "options": ["a) imports", "b) exports", "c) releases", "d) distributes"],
            "answer": "a) imports"
        },
        {
            "id": 22,
            "type": "mcq",
            "prompt": "To balance trade deficits, the nation aims to .... more finished manufactured goods to European markets.",
            "options": ["a) export", "b) import", "c) withhold", "d) retain"],
            "answer": "a) export"
        },
        {
            "id": 23,
            "type": "mcq",
            "prompt": "Over the past .... , the city transformed from a quiet town into a major industrial hub.",
            "options": ["a) decade", "b) second", "c) minute", "d) instant"],
            "answer": "a) decade"
        },
        {
            "id": 24,
            "type": "mcq",
            "prompt": "The annual medical .... brought together top specialists from across the continent to discuss new treatments.",
            "options": ["a) conference", "b) isolation", "c) division", "d) separation"],
            "answer": "a) conference"
        },
        {
            "id": 25,
            "type": "mcq",
            "prompt": "By wearing professional attire and delivering exceptional presentations, he always manages to .... in job interviews.",
            "options": ["a) stand out", "b) blend in", "c) fade away", "d) hide"],
            "answer": "a) stand out"
        },
        {
            "id": 26,
            "type": "mcq",
            "prompt": "The two engineering firms launched a .... venture to build the new high-speed railway line.",
            "options": ["a) joint", "b) single", "c) separated", "d) isolated"],
            "answer": "a) joint"
        },
        {
            "id": 27,
            "type": "mcq",
            "prompt": "Showing great academic .... , she solved complex calculus problems faster than anyone else in class.",
            "options": ["a) potential", "b) limitation", "c) weakness", "d) failure"],
            "answer": "a) potential"
        },
        {
            "id": 28,
            "type": "mcq",
            "prompt": "Small local shops can .... if they embrace online marketing tools and digital payment systems.",
            "options": ["a) flourish", "b) collapse", "c) wither", "d) stagnate"],
            "answer": "a) flourish"
        },
        {
            "id": 29,
            "type": "mcq",
            "prompt": "Students will greatly .... from reviewing past exam models before attempting final tests.",
            "options": ["a) benefit", "b) suffer", "c) lose", "d) decline"],
            "answer": "a) benefit"
        },
        {
            "id": 30,
            "type": "mcq",
            "prompt": "The tech startup designed a .... system that runs partly on battery and partly on solar energy.",
            "options": ["a) hybrid", "b) pure", "c) uniform", "d) single-source"],
            "answer": "a) hybrid"
        },
        {
            "id": 31,
            "type": "mcq",
            "prompt": "Operating a .... enterprise allows local craftsmen to manage production costs tightly while serving nearby neighborhoods.",
            "options": ["a) small-scale", "b) multinational", "c) continental", "d) massive"],
            "answer": "a) small-scale"
        },
        {
            "id": 32,
            "type": "mcq",
            "prompt": "The session moderator skillfully guided the debate, ensuring every .... had equal time to present their arguments.",
            "options": ["a) delegate", "b) outsider", "c) spectator", "d) observer"],
            "answer": "a) delegate"
        },
        {
            "id": 33,
            "type": "mcq",
            "prompt": "Continuous water management and modern .... systems are vital for expanding green spaces in dry regions.",
            "options": ["a) irrigation", "b) textile", "c) fund", "d) bridge"],
            "answer": "a) irrigation"
        },
        {
            "id": 34,
            "type": "mcq",
            "prompt": "The annual global economic .... focused on creating green investment opportunities for developing nations.",
            "options": ["a) summit", "b) division", "c) partition", "d) gap"],
            "answer": "a) summit"
        },
        {
            "id": 35,
            "type": "mcq",
            "prompt": "Having strong bilingual skills proved highly .... when dealing with international clients during the trade fair.",
            "options": ["a) advantageous", "b) disadvantageous", "c) harmful", "d) detrimental"],
            "answer": "a) advantageous"
        },
        {
            "id": 36,
            "type": "mcq",
            "prompt": "The committee met urgently to .... the rising public concerns regarding water resource distribution.",
            "options": ["a) address", "b) ignore", "c) overlook", "d) neglect"],
            "answer": "a) address"
        },
        {
            "id": 37,
            "type": "mcq",
            "prompt": "The heavy downpour during the night caused temporary transport disruptions across several .... regions.",
            "options": ["a) rural", "b) urban", "c) industrial", "d) metropolitan"],
            "answer": "a) rural"
        },
        {
            "id": 38,
            "type": "mcq",
            "prompt": "To double output efficiency, the factory floor underwent complete re-engineering and automation .... .",
            "options": ["a) upgrades", "b) regressions", "c) limitations", "d) reductions"],
            "answer": "a) upgrades"
        },
        {
            "id": 39,
            "type": "mcq",
            "prompt": "Effective cross-departmental .... ensures that marketing and technical teams stay aligned on product launches.",
            "options": ["a) collaboration", "b) isolation", "c) friction", "d) disorganization"],
            "answer": "a) collaboration"
        },
        {
            "id": 40,
            "type": "mcq",
            "prompt": "The exhibition showcased an impressive .... of historical artifacts spanning multiple dynasties.",
            "options": ["a) variety", "b) limitation", "c) shortage", "d) scarcity"],
            "answer": "a) variety"
        },
        {
            "id": 41,
            "type": "mcq",
            "prompt": "International trade agreements ensure that goods move across borders smoothly under agreed regulatory frameworks.",
            "options": ["a) goods", "b) wastes", "c) barriers", "d) blocks"],
            "answer": "a) goods"
        },
        {
            "id": 42,
            "type": "mcq",
            "prompt": "Investing surplus capital into innovative green enterprises is a sound strategy for long-term financial growth.",
            "options": ["a) invest", "b) spend", "c) waste", "d) lose"],
            "answer": "a) invest"
        },
        {
            "id": 43,
            "type": "mcq",
            "prompt": "The structural engineer inspected the newly built Nile bridge to confirm its resistance to heavy load stress.",
            "options": ["a) bridge", "b) tunnel", "c) trench", "d) canal"],
            "answer": "a) bridge"
        },
        {
            "id": 44,
            "type": "mcq",
            "prompt": "The entire educational staff participated in drafting the new school development framework.",
            "options": ["a) entire", "b) partial", "c) fraction", "d) segment"],
            "answer": "a) entire"
        },
        {
            "id": 45,
            "type": "mcq",
            "prompt": "Her impressive academic track record made her the top candidate for the presidential scholarship program.",
            "options": ["a) impressive", "b) ordinary", "c) dull", "d) mediocre"],
            "answer": "a) impressive"
        },
        {
            "id": 46,
            "type": "mcq",
            "prompt": "The moderation team ensured that all panel discussions proceeded smoothly without off-topic arguments.",
            "options": ["a) moderator", "b) instigator", "c) troublemaker", "d) outsider"],
            "answer": "a) moderator"
        },
        {
            "id": 47,
            "type": "mcq",
            "prompt": "Accelerated economic growth requires continuous support for small and medium-sized local enterprises.",
            "options": ["a) growth", "b) recession", "c) decline", "d) stagnation"],
            "answer": "a) growth"
        },
        {
            "id": 48,
            "type": "mcq",
            "prompt": "The corporation plans to scale up production capacity by integrating advanced artificial intelligence into assembly lines.",
            "options": ["a) scale up", "b) scale down", "c) close down", "d) halt"],
            "answer": "a) scale up"
        },
        {
            "id": 49,
            "type": "mcq",
            "prompt": "The desert reclamation project introduced drought-tolerant crop strains to secure food supplies.",
            "options": ["a) drought-tolerant", "b) water-wasting", "c) fragile", "d) delicate"],
            "answer": "a) drought-tolerant"
        },
        {
            "id": 50,
            "type": "mcq",
            "prompt": "Community-driven projects rely primarily on local volunteer efforts and grassroots participation.",
            "options": ["a) community-driven", "b) state-imposed", "c) foreign-dictated", "d) corporate-led"],
            "answer": "a) community-driven"
        },
        {
            "id": 51,
            "type": "tf",
            "prompt": "Scaling back a business operation implies expanding production lines and increasing workforce numbers rapidly.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 52,
            "type": "tf",
            "prompt": "Climate-resilient crops possess biological traits that help them survive extreme weather fluctuations and prolonged dry spells.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 53,
            "type": "tf",
            "prompt": "Solar-powered systems depend entirely on energy generated from burning organic fossil fuels.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 54,
            "type": "tf",
            "prompt": "A life-changing event is typically insignificant and has little to no permanent effect on an individual's career path.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 55,
            "type": "tf",
            "prompt": "Infrastructure investments involve developing foundational physical facilities such as transport, power grids, and communication networks.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 56,
            "type": "tf",
            "prompt": "Strategic partnerships are designed to foster long-term mutual cooperation between entities to achieve shared objectives.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 57,
            "type": "tf",
            "prompt": "System integration refers to the deliberate process of keeping different technological departments completely segregated from one another.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 58,
            "type": "tf",
            "prompt": "Operational stability ensures that a system functions smoothly without sudden collapses or erratic performance fluctuations.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 59,
            "type": "tf",
            "prompt": "A geographical gateway usually acts as a critical entry point or access route linking distinct regions or markets.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 60,
            "type": "tf",
            "prompt": "Textiles refer exclusively to heavy machinery and electronic hardware components used in factories.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 61,
            "type": "tf",
            "prompt": "Financial funding represents the capital resources allocated to support specific commercial projects or social initiatives.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 62,
            "type": "tf",
            "prompt": "Rural regions are characterized by dense high-rise skyscrapers, heavy traffic congestion, and industrial metropolitan environments.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 63,
            "type": "tf",
            "prompt": "Mutual respect implies a reciprocal relationship where each party values and honors the other equally.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 64,
            "type": "tf",
            "prompt": "Economic expansion refers to shrinking market reach and reducing overall national commercial output.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 65,
            "type": "tf",
            "prompt": "Advanced irrigation systems optimize agricultural water usage, ensuring crops receive adequate moisture in arid climates.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 66,
            "type": "tf",
            "prompt": "Attracting foreign investors requires establishing stable regulatory environments and robust economic infrastructure.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 67,
            "type": "tf",
            "prompt": "Budgetary limitations give project managers an infinite amount of financial resources to spend without restrictions.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 68,
            "type": "tf",
            "prompt": "Standard operating procedures are detailed guidelines established to maintain safety and consistency during critical medical tasks.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 69,
            "type": "tf",
            "prompt": "A national development initiative represents a structured plan implemented by authorities to address societal or economic challenges.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 70,
            "type": "tf",
            "prompt": "Importing goods involves selling domestic products to foreign buyers across international boundaries.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 71,
            "type": "tf",
            "prompt": "Exporting goods generates foreign revenue by shipping domestically produced items to international markets.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 72,
            "type": "tf",
            "prompt": "A decade spans exactly ten consecutive years in chronological measurement.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 73,
            "type": "tf",
            "prompt": "An academic conference serves as a formal gathering where researchers present findings and discuss professional developments.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 74,
            "type": "tf",
            "prompt": "To stand out in a competitive professional environment means to blend into the background and avoid notice completely.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 75,
            "type": "tf",
            "prompt": "A joint venture combines the resources of separate organizations to tackle a shared project successfully.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 76,
            "type": "tf",
            "prompt": "Academic potential refers to an inherent capacity for future growth, learning, and high achievement.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 77,
            "type": "tf",
            "prompt": "Market flourishment describes a state of economic decline, business closures, and widespread commercial failure.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 78,
            "type": "tf",
            "prompt": "Educational benefits refer to the positive gains and advantages students acquire from participating in quality courses.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 79,
            "type": "tf",
            "prompt": "A hybrid system combines two distinct technologies or methodologies to leverage the strengths of both.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 80,
            "type": "tf",
            "prompt": "Small-scale enterprises require massive multinational funding and thousands of employees to operate effectively.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 81,
            "type": "tf",
            "prompt": "A conference moderator is responsible for managing debate flow, keeping time, and organizing speaker participation.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 82,
            "type": "tf",
            "prompt": "Agricultural irrigation is completely unnecessary in regions experiencing extreme annual droughts.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 83,
            "type": "tf",
            "prompt": "An international political summit brings together heads of state to negotiate major global policies.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 84,
            "type": "tf",
            "prompt": "Advantageous circumstances provide favorable conditions that increase the likelihood of success.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 85,
            "type": "tf",
            "prompt": "Addressing a complex problem requires ignoring it until it resolves itself naturally.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 86,
            "type": "tf",
            "prompt": "Scaling up production means increasing manufacturing volume and operational capacity to meet higher demand.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 87,
            "type": "tf",
            "prompt": "Team collaboration hinders productivity by encouraging isolation and independent working styles.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 88,
            "type": "tf",
            "prompt": "A diverse product variety gives consumers multiple options tailored to different preferences and needs.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 89,
            "type": "tf",
            "prompt": "Commercial goods include physical items produced, bought, and sold within local and international markets.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 90,
            "type": "tf",
            "prompt": "Financial investment involves allocating capital into business ventures with the expectation of generating future returns.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 91,
            "type": "tf",
            "prompt": "A physical bridge serves to disconnect communities separated by natural barriers like rivers or valleys.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 92,
            "type": "tf",
            "prompt": "Involving the entire team means including every single member in the collective planning process.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 93,
            "type": "tf",
            "prompt": "An impressive performance fails to capture attention or leave any memorable impact on observers.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 94,
            "type": "tf",
            "prompt": "Economic growth is measured by an increase in the production of goods and services within an economy.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 95,
            "type": "tf",
            "prompt": "Drought-tolerant plants require constant heavy flooding and are unable to survive in dry environments.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 96,
            "type": "tf",
            "prompt": "Community-driven initiatives empower local residents to take charge of neighborhood development projects.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 97,
            "type": "tf",
            "prompt": "Urban regions are typically characterized by wide open agricultural fields, farms, and sparse populations.",
            "options": ["True", "False"],
            "answer": False
        },
        {
            "id": 98,
            "type": "tf",
            "prompt": "Mutual cooperation requires active participation and shared effort from all involved partners.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 99,
            "type": "tf",
            "prompt": "A stable employment contract provides a consistent and predictable source of steady income over time.",
            "options": ["True", "False"],
            "answer": True
        },
        {
            "id": 100,
            "type": "tf",
            "prompt": "Industrial manufacturing converts raw materials into finished consumer goods using specialized machinery.",
            "options": ["True", "False"],
            "answer": True
            }
    ],
       "محترف": [
            { 
            "id": 1,
            "type": "mcq",
            "prompt": "The government allocated a massive budget for the .... of rural villages to improve living standards.",
            "options": ["a) modernization", "b) isolation", "c) termination", "d) reduction"],
            "answer": "a) modernization"
        },
        {
            "id": 2,
            "type": "mcq",
            "prompt": "Successful business leaders know how to .... strategic partnerships with international companies.",
            "options": ["a) forge", "b) waste", "c) neglect", "d) abandon"],
            "answer": "a) forge"
        },
        {
            "id": 3,
            "type": "mcq",
            "prompt": "The newly launched economic .... aims to support small enterprises and boost local production.",
            "options": ["a) hurdle", "b) venture", "c) obstacle", "d) barrier"],
            "answer": "b) venture"
        },
        {
            "id": 4,
            "type": "mcq",
            "prompt": "Water scarcity requires farmers to adopt .... irrigation techniques to conserve every single drop.",
            "options": ["a) wasteful", "b) efficient", "c) random", "d) traditional"],
            "answer": "b) efficient"
        },
        {
            "id": 5,
            "type": "mcq",
            "prompt": "To remain competitive in the global market, the factory must upgrade its outdated .... .",
            "options": ["a) machinery", "b) decoration", "c) furniture", "d) stationery"],
            "answer": "a) machinery"
        },
        {
            "id": 6,
            "type": "mcq",
            "prompt": "The annual economic report showed a steady .... in the country's export rates.",
            "options": ["a) decline", "b) drop", "c) surge", "d) fall"],
            "answer": "c) surge"
        },
        {
            "id": 7,
            "type": "mcq",
            "prompt": "Building robust .... like roads, ports, and power grids is essential for attracting foreign investments.",
            "options": ["a) architecture", "b) infrastructure", "c) structure", "d) framework"],
            "answer": "b) infrastructure"
        },
        {
            "id": 8,
            "type": "mcq",
            "prompt": "The two nations signed a trade agreement to ensure .... benefits and equal commercial opportunities.",
            "options": ["a) one-sided", "b) mutual", "c) isolated", "d) single"],
            "answer": "b) mutual"
        },
        {
            "id": 9,
            "type": "mcq",
            "prompt": "Climate change poses a severe threat to agricultural output, making .... crop varieties a top priority.",
            "options": ["a) fragile", "b) weak", "c) resilient", "d) sensitive"],
            "answer": "c) resilient"
        },
        {
            "id": 10,
            "type": "mcq",
            "prompt": "The company managed to .... its annual profits through effective marketing and cost reduction.",
            "options": ["a) halve", "b) double", "c) drop", "d) split"],
            "answer": "b) double"
        },
        {
            "id": 11,
            "type": "mcq",
            "prompt": "Implementing modern technology into traditional classrooms facilitates a smooth educational .... .",
            "options": ["a) segregation", "b) separation", "c) integration", "d) division"],
            "answer": "c) integration"
        },
        {
            "id": 12,
            "type": "mcq",
            "prompt": "Engineers are working on a .... energy project that combines solar power with wind power.",
            "options": ["a) hybrid", "b) single", "c) pure", "d) isolated"],
            "answer": "a) hybrid"
        },
        {
            "id": 13,
            "type": "mcq",
            "prompt": "Cairo acts as a major economic .... connecting North African markets with the Middle East.",
            "options": ["a) cul-de-sac", "b) gateway", "c) barrier", "d) obstacle"],
            "answer": "b) gateway"
        },
        {
            "id": 14,
            "type": "mcq",
            "prompt": "Securing adequate .... is the primary challenge for startup founders looking to expand globally.",
            "options": ["a) debt", "b) funding", "c) loss", "d) penalty"],
            "answer": "b) funding"
        },
        {
            "id": 15,
            "type": "mcq",
            "prompt": "Unlike bustling metropolitan centers, .... regions offer a tranquil environment focused mainly on farming.",
            "options": ["a) urban", "b) rural", "c) industrial", "d) commercial"],
            "answer": "b) rural"
        },
        {
            "id": 16,
            "type": "mcq",
            "prompt": "High-quality .... produced in local Egyptian factories are now exported to international markets.",
            "options": ["a) textiles", "b) wastes", "c) scraps", "d) debris"],
            "answer": "a) textiles"
        },
        {
            "id": 17,
            "type": "mcq",
            "prompt": "The board of directors decided to .... the scope of operations to cover three new African countries.",
            "options": ["a) narrow", "b) restrict", "c) expand", "d) limit"],
            "answer": "c) expand"
        },
        {
            "id": 18,
            "type": "mcq",
            "prompt": "Strict safety .... must be followed inside pharmaceutical laboratories to prevent accidents.",
            "options": ["a) guesses", "b) procedures", "c) hazards", "d) risks"],
            "answer": "b) procedures"
        },
        {
            "id": 19,
            "type": "mcq",
            "prompt": "International .... is crucial for solving global challenges such as pollution and food insecurity.",
            "options": ["a) conflict", "b) cooperation", "c) hostility", "d) rivalry"],
            "answer": "b) cooperation"
        },
        {
            "id": 20,
            "type": "mcq",
            "prompt": "Despite facing severe financial constraints, the project demonstrated remarkable .... and survived.",
            "options": ["a) collapse", "b) stability", "c) failure", "d) weakness"],
            "answer": "b) stability"
        },
        {
            "id": 21,
            "type": "mcq",
            "prompt": "The startup launched an aggressive social media campaign to .... brand awareness among teenagers.",
            "options": ["a) undermine", "b) boost", "c) lower", "d) decrease"],
            "answer": "b) boost"
        },
        {
            "id": 22,
            "type": "mcq",
            "prompt": "Access to clean drinking water has been a .... development for the remote desert community.",
            "options": ["a) minor", "b) life-changing", "c) trivial", "d) negligible"],
            "answer": "b) life-changing"
        },
        {
            "id": 23,
            "type": "mcq",
            "prompt": "Small-scale farmers heavily rely on .... pumps to run their irrigation systems off the electrical grid.",
            "options": ["a) fuel-guzzling", "b) solar-powered", "c) manual-driven", "d) power-draining"],
            "answer": "b) solar-powered"
        },
        {
            "id": 24,
            "type": "mcq",
            "prompt": "The initiative focuses on empowering .... businesses run by young local entrepreneurs.",
            "options": ["a) massive", "b) multinational", "c) small-scale", "d) corporate"],
            "answer": "c) small-scale"
        },
        {
            "id": 25,
            "type": "mcq",
            "prompt": "Scientists developed .... crops capable of withstanding prolonged periods of severe drought.",
            "options": ["a) drought-tolerant", "b) water-hungry", "c) flood-prone", "d) moisture-loving"],
            "answer": "a) drought-tolerant"
        },
        {
            "id": 26,
            "type": "mcq",
            "prompt": "Local communities actively participated in the cleanup campaign, proving it to be truly .... .",
            "options": ["a) top-down", "b) community-driven", "c) state-enforced", "d) externally-funded"],
            "answer": "b) community-driven"
        },
        {
            "id": 27,
            "type": "mcq",
            "prompt": "The tech company decided to .... its production lines to meet the unexpected surge in market demand.",
            "options": ["a) scale up", "b) scale down", "c) wind down", "d) phase out"],
            "answer": "a) scale up"
        },
        {
            "id": 28,
            "type": "mcq",
            "prompt": "Due to budget cuts, the factory management was forced to .... operations in the secondary plant.",
            "options": ["a) scale up", "b) scale back", "c) step up", "d) speed up"],
            "answer": "b) scale back"
        },
        {
            "id": 29,
            "type": "mcq",
            "prompt": "Public figures must carefully .... pressing environmental issues during international summits.",
            "options": ["a) ignore", "b) address", "c) neglect", "d) overlook"],
            "answer": "b) address"
        },
        {
            "id": 30,
            "type": "mcq",
            "prompt": "In a room full of experienced researchers, her innovative methodology made her .... .",
            "options": ["a) blend in", "b) stand out", "c) fade away", "d) hide out"],
            "answer": "b) stand out"
        },
        {
            "id": 31,
            "type": "mcq",
            "prompt": "Egypt continues to .... raw materials and components needed for heavy manufacturing industries.",
            "options": ["a) export", "b) import", "c) release", "d) discharge"],
            "answer": "b) import"
        },
        {
            "id": 32,
            "type": "mcq",
            "prompt": "The country aims to .... high-value manufactured goods to neighboring African markets.",
            "options": ["a) import", "b) export", "c) buy", "d) purchase"],
            "answer": "b) export"
        },
        {
            "id": 33,
            "type": "mcq",
            "prompt": "Nations often .... goods and technologies to foster mutual economic growth and diplomatic ties.",
            "options": ["a) exchange", "b) withhold", "c) hoard", "d) confiscate"],
            "answer": "a) exchange"
        },
        {
            "id": 34,
            "type": "mcq",
            "prompt": "Over the past .... , technological advancements have completely transformed global communication.",
            "options": ["a) decade", "b) century", "c) millennium", "d) fortnight"],
            "answer": "a) decade"
        },
        {
            "id": 35,
            "type": "mcq",
            "prompt": "The government's national .... aims to plant millions of trees to combat desertification.",
            "options": ["a) obstacle", "b) initiative", "c) setback", "d) hindrance"],
            "answer": "b) initiative"
        },
        {
            "id": 36,
            "type": "mcq",
            "prompt": "Acquiring fluency in a second language gives students a distinct .... edge in the job market.",
            "options": ["a) disadvantageous", "b) advantageous", "c) detrimental", "d) harmful"],
            "answer": "b) advantageous"
        },
        {
            "id": 37,
            "type": "mcq",
            "prompt": "The economic summit brought together political leaders and corporate tycoons from across the .... .",
            "options": ["a) village", "b) continent", "c) neighborhood", "d) district"],
            "answer": "b) continent"
        },
        {
            "id": 38,
            "type": "mcq",
            "prompt": "Successful entrepreneurs view every market challenge as an opportunity to build a thriving .... .",
            "options": ["a) failure", "b) enterprise", "c) bankruptcy", "d) collapse"],
            "answer": "b) enterprise"
        },
        {
            "id": 39,
            "type": "mcq",
            "prompt": "She showed tremendous .... during her internship, impressing senior managers with her problem-solving skills.",
            "options": ["a) potential", "b) limitation", "c) restriction", "d) incapacity"],
            "answer": "a) potential"
        },
        {
            "id": 40,
            "type": "mcq",
            "prompt": "Hundreds of international delegates are expected to .... the upcoming global climate conference in Cairo.",
            "options": ["a) boycott", "b) attend", "c) skip", "d) evade"],
            "answer": "b) attend"
        },
        {
            "id": 41,
            "type": "mcq",
            "prompt": "Small local businesses can .... rapidly if they receive proper financial backing and mentorship.",
            "options": ["a) wither", "b) flourish", "c) stagnate", "d) decline"],
            "answer": "b) flourish"
        },
        {
            "id": 42,
            "type": "mcq",
            "prompt": "Participating in professional development workshops allows employees to .... immensely in their careers.",
            "options": ["a) suffer", "b) benefit", "c) lose", "d) regress"],
            "answer": "b) benefit"
        },
        {
            "id": 43,
            "type": "mcq",
            "prompt": "The entire engineering team worked overnight to fix the critical software bug before the system launch.",
            "options": ["a) partial", "b) entire", "c) fractional", "d) limited"],
            "answer": "b) entire"
        },
        {
            "id": 44,
            "type": "mcq",
            "prompt": "Her presentation on renewable energy was so .... that it received a standing ovation from the audience.",
            "options": ["a) uninspiring", "b) impressive", "c) dull", "d) tedious"],
            "answer": "b) impressive"
        },
        {
            "id": 45,
            "type": "mcq",
            "prompt": "The panel discussion was expertly guided by a neutral .... who ensured all viewpoints were heard.",
            "options": ["a) troublemaker", "b) moderator", "c) disruptor", "d) agitator"],
            "answer": "b) moderator"
        },
        {
            "id": 46,
            "type": "mcq",
            "prompt": "Rapid industrial .... has significantly boosted employment rates across urban centers.",
            "options": ["a) stagnation", "b) growth", "c) decline", "d) recession"],
            "answer": "b) growth"
        },
        {
            "id": 47,
            "type": "mcq",
            "prompt": "The newly built highway serves as a vital .... linking remote agricultural zones to major trade hubs.",
            "options": ["a) barrier", "b) bridge", "c) wall", "d) blockade"],
            "answer": "b) bridge"
        },
        {
            "id": 48,
            "type": "mcq",
            "prompt": "Retailers reported a massive increase in consumer demand for electronic .... ahead of the holiday season.",
            "options": ["a) services", "b) goods", "c) duties", "d) labors"],
            "answer": "b) goods"
        },
        {
            "id": 49,
            "type": "mcq",
            "prompt": "Wise investors prefer to .... their capital in sustainable, eco-friendly technological projects.",
            "options": ["a) waste", "b) invest", "c) squander", "d) gamble"],
            "answer": "b) invest"
        },
        {
            "id": 50,
            "type": "mcq",
            "prompt": "Despite strict regulations, the company faces certain technical .... regarding data privacy integration.",
            "options": ["a) advantages", "b) limitations", "c) benefits", "d) perks"],
            "answer": "b) limitations"
        },

        # --- ثانياً: أسئلة الصواب والخطأ الاحترافية (Advanced True or False) ---
        {
            "id": 51,
            "type": "tf",
            "prompt": "Economic stability implies that a financial system is immune to sudden, catastrophic collapses and operates steadily.",
            "answer": True
        },
        {
            "id": 52,
            "type": "tf",
            "prompt": "A textile refers strictly to raw metallic minerals extracted from deep underground mines.",
            "answer": False
        },
        {
            "id": 53,
            "type": "tf",
            "prompt": "Forming a formal partnership legally binds two or more entities to collaborate for shared commercial advantages.",
            "answer": True
        },
        {
            "id": 54,
            "type": "tf",
            "prompt": "Integration is the deliberate practice of segregating business units to prevent cross-departmental communication.",
            "answer": False
        },
        {
            "id": 55,
            "type": "tf",
            "prompt": "A hybrid model combines elements of two different systems to yield superior performance outcomes.",
            "answer": True
        },
        {
            "id": 56,
            "type": "tf",
            "prompt": "In a trade context, a geographical gateway functions as a critical entry point connecting broader regional markets.",
            "answer": True
        },
        {
            "id": 57,
            "type": "tf",
            "prompt": "Project funding is defined as the financial capital allocated specifically to support operational activities and development.",
            "answer": True
        },
        {
            "id": 58,
            "type": "tf",
            "prompt": "Rural settings are characterized by high-rise corporate skyscrapers, heavy traffic congestion, and dense populations.",
            "answer": False
        },
        {
            "id": 59,
            "type": "tf",
            "prompt": "Mutual cooperation relies on reciprocal efforts contributed equally by all involved parties.",
            "answer": True
        },
        {
            "id": 60,
            "type": "tf",
            "prompt": "Manufactured products are typically crafted individually by hand without the aid of industrial machinery.",
            "answer": False
        },
        {
            "id": 61,
            "type": "tf",
            "prompt": "National infrastructure encompasses core physical assets like transportation networks, electricity grids, and water systems.",
            "answer": True
        },
        {
            "id": 62,
            "type": "tf",
            "prompt": "Expanding a business enterprise means reducing its workforce, physical footprint, and market share.",
            "answer": False
        },
        {
            "id": 63,
            "type": "tf",
            "prompt": "Exporting involves shipping domestically produced goods and services to international buyers abroad.",
            "answer": True
        },
        {
            "id": 64,
            "type": "tf",
            "prompt": "Importing refers exclusively to selling domestic surplus products to foreign governments.",
            "answer": False
        },
        {
            "id": 65,
            "type": "tf",
            "prompt": "A demographic decade spans exactly ten consecutive calendar years.",
            "answer": True
        },
        {
            "id": 66,
            "type": "tf",
            "prompt": "A strategic initiative represents a planned, purposeful undertaking designed to resolve complex systemic issues.",
            "answer": True
        },
        {
            "id": 67,
            "type": "tf",
            "prompt": "Climate-resilient agricultural strains possess genetic adaptations allowing survival under volatile weather shocks.",
            "answer": True
        },
        {
            "id": 68,
            "type": "tf",
            "prompt": "Solar-powered installations draw their operational energy directly from photovoltaic conversion of sunlight.",
            "answer": True
        },
        {
            "id": 69,
            "type": "tf",
            "prompt": "Small-scale commercial ventures typically operate with localized reach, limited capital, and fewer employees.",
            "answer": True
        },
        {
            "id": 70,
            "type": "tf",
            "prompt": "Life-changing milestones exert a profound, long-lasting transformation on an individual's career or personal trajectory.",
            "answer": True
        },
        {
            "id": 71,
            "type": "tf",
            "prompt": "To scale up corporate production means scaling down output capacity and dismissing factory workers.",
            "answer": False
        },
        {
            "id": 72,
            "type": "tf",
            "prompt": "Scaling back operations is a deliberate managerial strategy to cut down expenses and production volumes.",
            "answer": True
        },
        {
            "id": 73,
            "type": "tf",
            "prompt": "Inter-agency cooperation requires synchronized teamwork directed toward achieving mutually beneficial outcomes.",
            "answer": True
        },
        {
            "id": 74,
            "type": "tf",
            "prompt": "An entrepreneurial enterprise is a commercial venture initiated and managed under private economic risk.",
            "answer": True
        },
        {
            "id": 75,
            "type": "tf",
            "prompt": "Agricultural irrigation systems utilize engineered networks to supply controlled amounts of water to crops.",
            "answer": True
        },
        {
            "id": 76,
            "type": "tf",
            "prompt": "A diplomatic summit denotes a high-level conference convened by heads of state to negotiate major treaties.",
            "answer": True
        },
        {
            "id": 77,
            "type": "tf",
            "prompt": "An advantageous proposal yields highly favorable, productive, and beneficial outcomes for participants.",
            "answer": True
        },
        {
            "id": 78,
            "type": "tf",
            "prompt": "A formal conference is characterized by casual gossip exchanged informally among strangers in public spaces.",
            "answer": False
        },
        {
            "id": 79,
            "type": "tf",
            "prompt": "An architectural bridge physically spans geographical obstacles to connect previously isolated territories.",
            "answer": True
        },
        {
            "id": 80,
            "type": "tf",
            "prompt": "Commercial entities flourish when they adapt rapidly to market innovations and consumer preferences.",
            "answer": True
        },
        {
            "id": 81,
            "type": "tf",
            "prompt": "Strict procedural compliance minimizes medical malpractice risks during complex surgical procedures.",
            "answer": True
        },
        {
            "id": 82,
            "type": "tf",
            "prompt": "Global economic interdependence ensures that a financial crisis in one continent never affects emerging markets.",
            "answer": False
        },
        {
            "id": 83,
            "type": "tf",
            "prompt": "Raw material processing transforms unprocessed natural substances into usable industrial components.",
            "answer": True
        },
        {
            "id": 84,
            "type": "tf",
            "prompt": "Sustainable development balances economic expansion with the long-term preservation of ecological resources.",
            "answer": True
        },
        {
            "id": 85,
            "type": "tf",
            "prompt": "Foreign direct investment injects critical capital into developing economies to accelerate modernization.",
            "answer": True
        },
        {
            "id": 86,
            "type": "tf",
            "prompt": "Urban migration patterns typically show a massive shift of populations from major industrial cities into remote deserts.",
            "answer": False
        },
        {
            "id": 87,
            "type": "tf",
            "prompt": "Comprehensive market research helps firms identify customer needs before launching new commercial products.",
            "answer": True
        },
        {
            "id": 88,
            "type": "tf",
            "prompt": "Diplomatic dialogue serves as the primary mechanism for resolving international trade disputes peacefully.",
            "answer": True
        },
        {
            "id": 89,
            "type": "tf",
            "prompt": "Technological innovation frequently renders older industrial methodologies obsolete within competitive markets.",
            "answer": True
        },
        {
            "id": 90,
            "type": "tf",
            "prompt": "Cross-border trade agreements are designed primarily to erect bureaucratic trade barriers between friendly nations.",
            "answer": False
        },
        {
            "id": 91,
            "type": "tf",
            "prompt": "Operational efficiency guarantees that manufacturing companies waste minimal resources while maximizing output quality.",
            "answer": True
        },
        {
            "id": 92,
            "type": "tf",
            "prompt": "Human capital investment focuses on improving workforce skills through specialized training and education programs.",
            "answer": True
        },
        {
            "id": 93,
            "type": "tf",
            "prompt": "Macroeconomic indicators such as inflation rates directly influence consumer spending habits and market stability.",
            "answer": True
        },
        {
            "id": 94,
            "type": "tf",
            "prompt": "Supply chain disruptions can severely paralyze international manufacturing networks and delay product delivery.",
            "answer": True
        },
        {
            "id": 95,
            "type": "tf",
            "prompt": "Environmental regulations compel industrial factories to reduce carbon footprints and adopt green technologies.",
            "answer": True
        },
        {
            "id": 96,
            "type": "tf",
            "prompt": "Strategic planning enables corporate executives to anticipate future market shifts and allocate resources efficiently.",
            "answer": True
        },
        {
            "id": 97,
            "type": "tf",
            "prompt": "Economic globalization isolates domestic markets completely from international trade fluctuations and foreign competition.",
            "answer": False
        },
        {
            "id": 98,
            "type": "tf",
            "prompt": "Public-private partnerships combine government backing with private sector innovation to execute mega infrastructure projects.",
            "answer": True
        },
        {
            "id": 99,
            "type": "tf",
            "prompt": "Rigorous quality control protocols ensure that manufactured goods meet safety standards before reaching consumers.",
            "answer": True
        },
        {
            "id": 100,
            "type": "tf",
            "prompt": "Continuous professional development empowers teachers to implement modern pedagogical strategies inside classrooms successfully.",
            "answer": True
        }
  ]
}
@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
   
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB.get("متوسط", []))
   
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
       
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else []
        session['questions'] = selected_questions
        session['level'] = level
        session['current_index'] = 0
        session['user_answers'] = {}
        return redirect(url_for('quiz_step'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_step():
    questions = session.get('questions', [])
    current_index = session.get('current_index', 0)
    level = session.get('level', 'متوسط')
   
    if not questions:
        return redirect(url_for('index'))
       
    if request.method == 'POST':
        ans = request.form.get('current_answer')
        
        user_answers = session.get('user_answers', {})
        user_answers[str(current_index)] = {
            "prompt": questions[current_index]['prompt'],
            "user_ans": ans if ans else "لم تتم الإجابة",
            "correct_ans": questions[current_index]['answer'],
            "is_correct": (ans == questions[current_index]['answer'])
        }
        session['user_answers'] = user_answers
       
        current_index += 1
        session['current_index'] = current_index
       
    if current_index >= len(questions):
        return redirect(url_for('results'))
       
    current_question = questions[current_index]
   
    return render_template_string(
        QUIZ_TEMPLATE,
        level=level,
        question=current_question,
        current_num=current_index + 1,
        total_questions=len(questions),
        num_questions=len(questions)
    )

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    level = session.get('level', 'متوسط')
   
    score = 0
    total = len(user_answers)
    results_list = []
   
    for idx, data in sorted(user_answers.items(), key=lambda x: int(x[0])):
        if data['is_correct']:
            score += 1
        results_list.append({
            "id": int(idx) + 1,
            "prompt": data['prompt'],
            "user_ans": data['user_ans'],
            "correct_ans": data['correct_ans'],
            "is_correct": data['is_correct']
        })
       
    return render_template_string(
        RESULT_TEMPLATE,
        level=level,
        score=score,
        total=total,
        results=results_list
    )

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
       
        <form method="POST">
            <input type="hidden" name="action" value="generate">
            <div class="section-title">اختيار مستوى الصعوبة الدرس الاول اللغة الإنجليزية 2ث ازهر</div>
            <div class="levels-container">
                <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                    <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                </label>
                <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                    <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                </label>
                <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
           
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="5" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
           
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
       
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
    </div>
    <script>
        function updateActive(radio) {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            radio.closest('.level-btn').classList.add('active');
        }
    </script>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        #timer-box { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 16px; display: none; }
        @media print {
            body { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">السؤال: <strong style="color: #114b3e;">{{ current_num }} من {{ total_questions }}</strong></span>
        </div>

        <h2>اختبار الدرس الأول الشامل</h2>
       
        <form method="POST" action="{{ url_for('quiz_step') }}" id="quiz-form">
            <div class="question-box">
                <span class="badge-type">اختيار من متعدد</span>
                <p><strong>سؤال {{ current_num }}:</strong> {{ question.prompt }}</p>
               
                <div class="options-list">
                    {% for opt in question.options %}
                        <label class="option-item">
                            <input type="radio" name="current_answer" value="{{ opt }}" required> {{ opt }}
                        </label>
                    {% endfor %}
                </div>
                <div class="hint">💡 <em>{{ question.hint }}</em></div>
            </div>
           
            <button type="submit" class="start-btn">السؤال التالي ←</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
       
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <button type="button" class="start-btn print-btn" onclick="window.print()" style="background: #455a64; margin-top: 15px;">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
