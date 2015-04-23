# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.core.management.base import BaseCommand, CommandError
from spirit.models.category import Category
from spirit.models.topic import Topic
from spirit.models.comment import Comment
from member.models import Member
from server.models import Server, Volunteer
from gfe.settings import *
from faker import Factory
import random
from datetime import datetime
import pytz
from django.db import transaction
import cProfile, pstats, StringIO, string
from django.contrib.auth.hashers import make_password

# Todo: Password for users
# empty database tables?

class Command(BaseCommand):
	args = '<dodemo>'
	help = 'Fills the database with the required minimum data. dodemo, when used, creates demonstration data. dodemopassword is the password that all fake users passwords are set to'
	
	
	# Some arrays with nice looking fake data, for use when randomly generating servers, volunteers etc.
	
	animals = ["Penguin", "Zebra", "Cat", "Giraffe", "Horse", "Lion","Narwhaal"]
	words = ["awesome", "breathtaking", "amazing", "stunning", "astounding", "astonishing", "awe-inspiring", "stupendous", "staggering", "extraordinary", "incredible", "unbelievable"]
	games = ["Minecraft", "Counter Strike", "FTL", "Minesweeper", "World of warcraft", "Trouble in Terrorist Town", "Prop hunt"]
	categories = ["Shoot'em'ups", "Competitions", "Minecraft", "Open Discussion", "Website", "Membership", "Development"]
	# These are not like, special codewords or anything. Just strings. The lorem ipsum single word thing looked shit ;)
	ranks = ["Moderator", "Flibmeister", "Operator", "Administrator", "Admin", "Fluffheimer", "Derpester", "Volunteer-inator"]
	
	members = [] # A place to hold all the members we create
	adminuser = None # The admin generated
	admin_pass = ""
	unpriv_user1 = None # Two unpriviliged users
	unpriv_pass1 = ""
	unpriv_user2 = None
	unpriv_pass2 = ""
	
	Faker = None
	
	def create_random_member(self, is_admin=False):
		first_name = self.Faker.first_name()
		last_name = self.Faker.last_name()
		username=self.Faker.user_name()
		email = self.Faker.email()
		phone = self.Faker.phone_number()
		password = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))
		date = self.Faker.date()
		city = self.Faker.city()
		postcode = self.Faker.postcode()
		adress = self.Faker.street_address()
		mem = Member(username=email,
			first_name=first_name,
			last_name=last_name,
			email=email,
			nick=username,
			birthdate=date,
			phone=phone,
			mobile='',
			street=adress,
			city=city,
			country_id="AF",
			zip=postcode,
			careof='',
			socialsecuritynumber='',
			refreshedon=datetime.now(pytz.timezone("GMT")),
			is_opt_in=self.Faker.boolean(90),
			password=make_password(password, None, 'md5'), # Hang on, md5? Yes. Django uses secure hashing by default, which without specifying a weak hashing algorithm makes this script take several minutes to run.
			is_superuser=is_admin,
			is_moderator=is_admin,
			is_staff=is_admin
		)
		
		#mem.set_password(dodemopassword)
		mem.save()
		self.members.append(mem)
		return {"member": mem, "password": password }
	
	def handle(self, *args, **options):
		#pr = cProfile.Profile()
		#pr.enable()
		transaction.set_autocommit(False)
		
		self.Faker = Factory.create()
		
		dodemo = False
		dodemopassword = ''
		
		try:
			dodemo = True if args[0] == '1' else False
			dodemopassword = args[1]
		except:
			pass
		
		# Set up a default seed so developers can talk to eachother
		self.Faker.seed(10000)
		
		# First, spirit needs us to create some categories for it to work at all:
		
		self.stdout.write("Filling up the standard categories\n")
		
		cat = Category(title="Private",slug="private",description="The category for all private discussions", is_closed=0, is_removed=0, is_private=0)
		cat.save()
		transaction.commit()
		if(cat.pk != ST_TOPIC_PRIVATE_CATEGORY_PK):
			raise CommandError("The id for the private category does not match up with our default in the settings. Check ST_TOPIC_PRIVATE_CATEGORY_PK, should be %d but is %d " % (ST_TOPIC_PRIVATE_CATEGORY_PK, cat.pk))
		
		cat = Category(title="Uncategorized",slug="uncategorized",description="The category for all uncategorized discussions", is_closed=0, is_removed=0, is_private=0)
		cat.save()
		transaction.commit()
		if(cat.pk != ST_UNCATEGORIZED_CATEGORY_PK):
			raise CommandError("The id for the uncategorized category does not match up with our default in the settings. Check ST_UNCATEGORIZED_CATEGORY_PK, should be %d but is %d " % (ST_UNCATEGORIZED_CATEGORY_PK, cat.pk))

		cat = Category(title="Other",slug="other",description="The category for external (server) discussions", is_closed=0, is_removed=0, is_private=0)
		cat.save()
		transaction.commit()
		if(cat.pk != ST_OTHER_CATEGORY_PK):
			raise CommandError("The id for the other category does not match up with our default in the settings. Check ST_OTHER_CATEGORY_PK, should be %d but is %d " % (ST_OTHER_CATEGORY_PK, cat.pk))
			
		if dodemo:
			self.stdout.write("Starting the fill of demo data\n")
		
			# Here is where we generate some categories
			
			cat_list = []
			
			self.stdout.write("Creating some fake categories\n")
			
			for str in self.categories:
				cat = Category(title=str,description="The category for all discussions about " + str, is_closed=0, is_removed=0, is_private=0)
				cat.save()
				cat_list.append(cat)
			
			transaction.commit()
			
			# Here is where we generate a couple of servers
			
			self.stdout.write("Creating some fake servers\n")
			
			servers = []
			
			for i in range(0, 100):
				name = random.choice(self.animals) + "'s " + random.choice(self.words) + " " + random.choice(self.games)
				server = Server(name=name, description=self.Faker.sentence() + " " +self.Faker.sentence(), howto="howto here", rules="rules here", questions="questions here", image='tuxie.jpg', image_height=0, image_width=0)
				server.save()
				servers.append(server)

			transaction.commit()
			
			# Create three users. One Admin, two unpriviliged users
			
			mem = self.create_random_member(True)
			
			adminuser = mem["member"] # The admin generated
			admin_pass = mem["password"]
			
			mem = self.create_random_member()
			
			unpriv_user1 = mem["member"] # Two unpriviliged users
			unpriv_pass1 = mem["password"]
			
			mem = self.create_random_member()
			
			unpriv_user2 = mem["member"]
			unpriv_pass2 = mem["password"]
			
			# Now generate a motherload of them
			
			for i in range(0,1000):
				self.create_random_member()
			
			self.stdout.write("Creating some fake members (may take a while)\n")
			
			transaction.commit()
			
			self.stdout.write("Creating some fake volunteers\n")
			
			# Here is where we generate a couple of volunteers
			statuscodes = ["OK", "WAITING", "DENIED"]
			
			for i in range(0, 300):
				vol = Volunteer(member=random.choice(self.members),
					server=random.choice(servers),
					answer=self.Faker.text(),
					role=self.Faker.word(),
					status=random.choice(statuscodes),
					sec_edit=self.Faker.boolean(),
					sec_accept=self.Faker.boolean()
				)
				vol.save()
				
			# Finally some topics
			
			transaction.commit()
			
			self.stdout.write("Creating some fake threads (may take a while!)\n")
			
			for i in range(0, 1000):
				top = Topic(user=random.choice(self.members),
					category=random.choice(cat_list),
					title=self.Faker.sentence(),
					is_pinned=self.Faker.boolean(5),
					is_closed=self.Faker.boolean(5),
					is_removed=self.Faker.boolean(5)
				)
				
				top.save()
				
				# Aaand some comments
				for z in range(0, random.randint(1, 500)):
					text = self.Faker.text()
					comm = Comment(user=random.choice(self.members),
						topic=top,
						comment=text,
						comment_html=text
					)
					comm.save()
			
			transaction.commit()
			
			self.stdout.write("Done! Below are three sample users of the 1003 we created:")
			self.stdout.write("Admin username:			"+adminuser.username+"		Admin password: "+admin_pass+"\n")
			self.stdout.write("Unprivileged username sample 1:	"+unpriv_user1.username+"		Unprivileged user 1 password: "+unpriv_pass1+"\n")
			self.stdout.write("Unprivileged username sample 1:	"+unpriv_user2.username+"	Unprivileged user 2 password: "+unpriv_pass2+"\n")
			#pr.disable()
			#s = StringIO.StringIO()
			#sortby = 'cumulative'
			#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
			#ps.print_stats()
			#self.stdout.write(s.getvalue())
		return