from BotnoiDevPlatform import *

## setup botnoi chatbot server

BN_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJibi1haWQiOiI2NTA5NmI0N2EwMjY0MWMyMjRiNWViNzciLCJibi11aWQiOiI2NDkzY2RjMjgyMjY1ODQxZTUwNTkzNDIiLCJpYXQiOjE2OTUxMTYxNjEsImp0aSI6IjEyOWQxNDk1LWVkMTQtNGI4Mi04ODlhLWJhNGY5ZTZjMzgyNSIsIm5iZiI6MTY5NTExNjE2MX0.FjQItXWRexM0h-DPam83JJ01nGj9bPhez3GhCnf2bv8"
BotnoiChatbotServer.setup_client(BN_API_KEY)
server = BotnoiChatbotServer()

## create a bot
test_bot = Bot(
    botName="test",
    botAvatar="https://console.botnoi.ai/assets/botnoi-logo/botnoi.svg",
    businessType="test",
    sex="male",
    age=20,
) # create a bot with name "test"
server.create_bot(test_bot) # add the bot to the server
test_bot.reload() # reload the bot from the server

## find a bot

test_bot = server.find_bot_with_name("test") # find a bot with name "test"

print(test_bot.to_json())

## create an intent

test_intent = Intent(name="test_intent") # create an intent with name "test_intent"
test_bot.opt.create_intent(test_intent) # add the intent to the server in the "test" bot
test_intent.reload() # reload the intent from the server

## find an intent
test_intent = test_bot.opt.find_intent_with_name("test_intent") # find an intent with name "test_intent"

print(test_intent.to_json())

## train an intent with keywords and reacitons

test_intent.opt.train_keyword(IntentKeyword("hello test")) # add a keyword "hello test" to the intent

test_intent.opt.train_reaction(IntentReaction(["hello! it works!"])) # add a reaction "hello! it works!" to the intent

## train an intent with multiple keywords and more advanced reacitons

test_intent.opt.train_multi_keyword(
    strings = ["hello test 2", "hello test 3"]
) # add multiple keywords to the intent

test_intent.opt.train_reaction(
    IntentReaction([
        Action.createParameter(parameterName="test_param", parameterValue=Action.get_keyword()), # create a parameter with name "test_param" and value of the user's keyword
        Action.text("test param is " + Action.parameter("test_param")), # get the parameter with name "test_param" and use it in the text,
        Action.image("test_image"), # send an image with name "test_image"
    ])
) # add a reaction to the intent

# ## create an image object

test_image_object = Object(
    objectName="test_image",
    objects=[
        ImageObject(
            original_url="https://console.botnoi.ai/assets/botnoi-logo/botnoi.svg",
            preview_image_url="https://console.botnoi.ai/assets/botnoi-logo/botnoi.svg",
        )
    ]
) # create an image object with name "test_image"
test_bot.opt.create_object(test_image_object) # add the object to the server in the "test" bot

## find an object

test_image_object = test_bot.opt.find_object_with_name("test_image",type=ObjectType.image()) # find an object with name "test_image"

print(test_image_object.to_json())