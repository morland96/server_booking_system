import mongoengine

mongoengine.connect("TEST")


class User(mongoengine.Document):
    username = mongoengine.StringField()
    a = mongoengine.StringField()


class Post(mongoengine.Document):
    owner = mongoengine.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    a = mongoengine.StringField()


User.drop_collection()
Post.drop_collection()
u = User()
u.username = "t"
u.a = "lsdkf"
u.save()
p = Post()
p.owner = u
p.a = "sdfsd"
p.save()
u.delete()
