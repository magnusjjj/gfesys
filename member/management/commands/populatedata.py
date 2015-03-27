from django.core.management.base import BaseCommand, CommandError
from spirit.models.category import Category
from spirit.models.topic import Topic
from spirit.models.comment import Comment
from member.models import Member
from server.models import Server, Volunteer
from gfe.settings import *
from faker import Faker as Fakey
import random
from datetime import datetime
import pytz

# Todo: Password for users
# empty database tables?

class Command(BaseCommand):
	args = '<dodemo dodemopassword>'
	help = 'Fills the database with the required minimum data. If you want to reset the tables used, also add "reset" to the command line. dodemo, when used, creates demonstration data.'
	
	def handle(self, *args, **options):
		
		Faker = Fakey()
		
		reset = False
		dodemo = False
		dodemopassword = ''
		
		try:
			dodemo = True if args[0] == '1' else False
			dodemopassword = args[1]
		except:
			pass
		
		# Set up a default seed so developers can talk to eachother
		Faker.seed(10000)
		
		# First, spirit needs us to create some categories for it to work at all:
		
		cat = Category(title="Private",slug="private",description="The category for all private discussions", is_closed=0, is_removed=0, is_private=0)
		cat.save()
		if(cat.pk != ST_TOPIC_PRIVATE_CATEGORY_PK):
			raise CommandError("The id for the private category does not match up with our default in the settings. Check ST_TOPIC_PRIVATE_CATEGORY_PK, should be %d but is %d " % (ST_TOPIC_PRIVATE_CATEGORY_PK, cat.pk))
		
		cat = Category(title="Uncategorized",slug="uncategorized",description="The category for all uncategorized discussions", is_closed=0, is_removed=0, is_private=0)
		cat.save()
		if(cat.pk != ST_UNCATEGORIZED_CATEGORY_PK):
			raise CommandError("The id for the uncategorized category does not match up with our default in the settings. Check ST_UNCATEGORIZED_CATEGORY_PK, should be %d but is %d " % (ST_UNCATEGORIZED_CATEGORY_PK, cat.pk))

		cat = Category(title="Other",slug="other",description="The category for external (server) discussions", is_closed=0, is_removed=0, is_private=0)
		cat.save()
		if(cat.pk != ST_OTHER_CATEGORY_PK):
			raise CommandError("The id for the other category does not match up with our default in the settings. Check ST_OTHER_CATEGORY_PK, should be %d but is %d " % (ST_OTHER_CATEGORY_PK, cat.pk))
		
		if dodemo:
			# Here is where we generate some categories
			
			animals = ["Penguin", "Zebra", "Cat", "Giraffe", "Horse", "Lion","Narwhaal"]
			words = ["awesome", "breathtaking", "amazing", "stunning", "astounding", "astonishing", "awe-inspiring", "stupendous", "staggering", "extraordinary", "incredible", "unbelievable"]
			games = ["Minecraft", "Counter Strike", "FTL", "Minesweeper", "World of warcraft", "Trouble in Terrorist Town", "Prop hunt"]
			categories = ["Shoot'em'ups", "Competitions", "Minecraft", "Open Discussion", "Website", "Membership", "Development"]
			
			for str in categories:
				cat = Category(title=str,slug=str.lower(),description="The category for all discussions about " + str, is_closed=0, is_removed=0, is_private=0)
				cat.save()
			
			# Here is where we generate a couple of servers
			
			servers = []
			
			for i in range(0, 100):
				name = random.choice(animals) + "'s " + random.choice(words) + " " + random.choice(games)
				server = Server(name=name, description=Faker.sentence() + " " +Faker.sentence(), howto="howto here", rules="rules here", questions="questions here", image='tuxie.jpg', image_height=0, image_width=0)
				server.save()
				servers.append(server)
			
			# Here is where we generate a couple of members
			
			members = []
			
			for i in range(0,1000):
				email = Faker.email()
				phone = Faker.phone_number()
				
				mem = Member(is_superuser=False,
					username='',
					first_name=Faker.first_name(),
					last_name=Faker.last_name(),
					email=email,
					nick=Faker.user_name(),
					birthdate=Faker.date(),
					phone=phone,
					mobile='',
					street=Faker.street_address(),
					city=Faker.city(),
					country_id="AF",
					zip=Faker.postcode(),
					careof='',
					socialsecuritynumber='',
					refreshedon=datetime.now(pytz.timezone("GMT")),
					is_opt_in=Faker.boolean(90)
				)
				
				mem.set_password(dodemopassword)
				mem.save()
				members.append(mem)
			
			# Here is where we generate a couple of volunteers
			statuscodes = ["OK", "WAITING", "DENIED"]
			
			for i in range(0, 300):
				vol = Volunteer(member=random.choice(members),
					server=random.choice(servers),
					answer=Faker.text(),
					role=Faker.word(),
					status=random.choice(statuscodes),
					sec_edit=Faker.boolean(),
					sec_accept=Faker.boolean()
				)
				
			# Finally some topics
			
			for i in range(0, 1000):
				top = Topic(user=random.choice(members),
					category=random.choice(categories),
					title=Faker.sentence(),
					is_pinned=Faker.boolean(5),
					is_closed=Faker.boolean(5),
					is_removed=Faker.boolean(5)
				)
				
				top.save()
				
				# Aaand some comments
				for z in range(0, random.randint(1, 500)):
					text = Faker.text()
					comm = Comment(user=random.choice(members),
						topic=top,
						comment=text,
						comment_html=text
					)
					comment.save()
		return