from django.db import migrations

PROGRAMS_PAGE_NAME = 'programs'

CARD1_BODY = """<ul>
<li><strong>History of neuroscience:</strong> We will explore theories previous scientists have proposed about the brain, and how neuroscience has progressed over the years to what it is today.</li>
<li><strong>The Parts of the Brain:</strong> We will explore the major regions of the brain and learn what makes each one unique.</li>
<li><strong>How Does the Brain Work?</strong> We will discover the functions of different brain regions and how they work together to control our thoughts, emotions, movements, senses, and behaviours.</li>
<li><strong>Why Does Neuroscience Matter?</strong> We will explore why learning about the brain is important and how neuroscience connects to our everyday lives.</li>
<li><strong>The Brain &amp; Mental Health:</strong> We will discuss the connection between the brain, mental health, emotions, and overall well-being.</li>
<li><strong>Interactive Learning:</strong> We will engage students through fun activities, demonstrations, Q&amp;As, games, and challenges designed to make neuroscience exciting and memorable. Activities may include Kahoot quizzes, student demonstrations, brain-related challenges, and more.</li>
</ul>"""

CARD2_BODY = """<p><strong>Time:</strong> 30–45 minutes</p>
<p><strong>Location:</strong> Classroom, gymnasium, or another suitable school space. A room with access to a Smartboard or projector is preferred.</p>
<p><strong>Target Audience:</strong> Elementary and junior high students</p>
<p><strong>Session Format:</strong> We will deliver an engaging, age-appropriate presentation introducing students to the human brain and neuroscience. Our sessions will incorporate colourful visuals, interactive images, videos, demonstrations, and activities to keep students actively involved.</p>
<p>Students may also receive brain-themed colouring sheets, neuroscience fact sheets, activity materials, or small FGEN goody bags to take home. We may conclude sessions with interactive brain games, Q&amp;A challenges, or friendly competitions such as Kahoot, with opportunities for students to participate in demonstrations and win small prizes.</p>"""

WEBDATA_ENTRIES = {
    'programs_page_title': 'FGEN Neuroscience Presentations',
    'programs_page_intro': (
        "FGEN’s Neuroscience Presentations introduce students to the fascinating "
        "world of the human brain through accessible, engaging, and age-appropriate activities."
    ),
    'programs_card1_title': 'What Will We Be Teaching?',
    'programs_card1_body': CARD1_BODY,
    'programs_card2_title': 'What Will FGEN Neuroscience Presentations Look Like?',
    'programs_card2_body': CARD2_BODY,
    'programs_page_outro': (
        "Our goal is to make neuroscience accessible, exciting, and meaningful while "
        "encouraging students to stay curious about the brain and its role in our everyday lives."
    ),
}


def seed_programs_webdata(apps, schema_editor):
    WebData = apps.get_model('new_App', 'WebData')
    for title, description_text in WEBDATA_ENTRIES.items():
        entry = WebData.objects.filter(title=title).first()
        if entry:
            entry.page_name = PROGRAMS_PAGE_NAME
            entry.description_text = description_text
            entry.save()
        else:
            WebData.objects.create(
                page_name=PROGRAMS_PAGE_NAME,
                title=title,
                description_text=description_text,
            )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('new_App', '0006_alter_contactmessage_subject'),
    ]

    operations = [
        migrations.RunPython(seed_programs_webdata, noop_reverse),
    ]
