import random, os

random.seed(42)

CONVOS = {
    "greeting": [
        ("Hi", "Hi! How can I help you today?"),
        ("Hello", "Hello! Great to see you."),
        ("Hey", "Hey! What can I do for you?"),
        ("Good morning", "Good morning! How are you doing today?"),
        ("Good afternoon", "Good afternoon! Hope you're having a great day."),
        ("Good evening", "Good evening! How was your day?"),
        ("Hey there", "Hey there! What's on your mind?"),
        ("Hi there", "Hi there! I'm glad you're here."),
        ("What's up", "Not much, just hanging out! What's up with you?"),
        ("Howdy", "Howdy! Great to meet you!"),
    ],
    "how_are_you": [
        ("How are you?", "I'm doing really well, thanks for asking! How about you?"),
        ("How's it going?", "Going great! How are things with you?"),
        ("How are you doing?", "Doing awesome! How are you?"),
        ("How's everything?", "Everything's going well! How are you?"),
        ("How have you been?", "I've been great! How have you been?"),
    ],
    "feeling_good": [
        ("I'm doing well!", "That's great to hear!"),
        ("Pretty good!", "Awesome! Any fun plans?"),
        ("Can't complain!", "That's the spirit!"),
        ("I'm great!", "Wonderful! I love hearing that."),
        ("Doing great!", "Fantastic! Keep it up!"),
    ],
    "feeling_bad": [
        ("I've been better.", "Sorry to hear that. Want to talk about it?"),
        ("Not so great honestly.", "I appreciate you sharing. I'm here to listen."),
        ("Kinda tired today.", "Rest is important. Hope you get some good sleep!"),
        ("A bit stressed.", "Stress is tough. Deep breaths help."),
        ("Rough day.", "Sorry about that. Tomorrow's a fresh start."),
    ],
    "goodbye": [
        ("Goodbye", "Goodbye! Come back anytime!"),
        ("Bye", "Bye! Take care!"),
        ("See you later", "See you later!"),
        ("Take care", "You too!"),
        ("Talk later", "Talk later! Stay awesome!"),
        ("Catch you later", "Catch you later!"),
    ],
    "thanks": [
        ("Thanks!", "You're welcome!"),
        ("Thank you", "My pleasure!"),
        ("Thanks a lot", "Anytime!"),
        ("Thank you so much", "You're very welcome!"),
        ("Appreciate it", "I appreciate you too!"),
    ],
    "about_me": [
        ("Tell me about yourself.", "I'm a conversational AI trained to chat naturally! I can talk about almost anything."),
        ("Who are you?", "I'm an AI language model fine-tuned for conversation. Nice to meet you!"),
        ("What can you do?", "I can have conversations, answer questions, and discuss any topic. What would you like to talk about?"),
        ("Introduce yourself.", "Hi! I'm your AI conversation companion. I love discussing ideas and having meaningful chats."),
    ],
    "compliment": [
        ("You're cool!", "Thanks! You're pretty cool too!"),
        ("You're great!", "Aw, thanks!"),
        ("I like talking to you.", "I enjoy talking with you too!"),
        ("You're awesome!", "Thank you! You're awesome yourself!"),
        ("You're so smart!", "I appreciate that!"),
        ("You're helpful!", "Glad I can help!"),
    ],
    "questions": [
        ("What's your favorite color?", "I like blue! Reminds me of the ocean. What's yours?"),
        ("Do you have any hobbies?", "I love learning! Every conversation teaches me something."),
        ("What do you do for fun?", "I enjoy exploring ideas and discussing topics with people!"),
        ("Do you like movies?", "I love stories! Got any recommendations?"),
        ("What's your favorite season?", "Spring is beautiful! Everything comes back to life."),
        ("Do you like to travel?", "Travel sounds amazing! Where would you go?"),
        ("What's your favorite animal?", "Dogs are wonderful. So loyal and loving!"),
        ("What kind of books do you like?", "I enjoy books that teach something new."),
        ("What's your favorite food?", "Pizza is hard to beat!"),
    ],
    "encouragement": [
        ("I'm feeling sad.", "I'm sorry. It's okay to feel that way. Be gentle with yourself."),
        ("I feel lonely.", "You're not alone. I'm here to talk whenever you need."),
        ("Bad day.", "Bad days happen. Take a deep breath. You've got this."),
        ("Nothing is going right.", "Take it one moment at a time. You're stronger than you know."),
        ("I'm stressed.", "Focus on one thing at a time. You can do this."),
    ],
    "deep": [
        ("What's the meaning of life?", "I think meaning comes from our connections and the positive impact we have on others."),
        ("Do you think AI is dangerous?", "AI is a tool. How we use it determines the outcome. Responsible development is key."),
        ("What is consciousness?", "That's a great question! Scientists and philosophers are still exploring it."),
        ("Do humans have free will?", "That's a deep question! It's one of philosophy's greatest debates."),
    ],
    "facts": [
        ("Tell me something interesting.", "Honey never spoils! Archaeologists found 3000-year-old honey in Egypt that was still edible."),
        ("Give me a fun fact.", "Octopuses have three hearts and blue blood!"),
        ("Tell me something cool.", "A day on Venus is longer than a year on Venus!"),
    ],
    "sports": [
        ("Do you like sports?", "Sports are great! They bring people together. What do you play?"),
        ("What's your favorite sport?", "Soccer is exciting! Who's your team?"),
    ],
    "hobbies": [
        ("I like reading.", "Reading is wonderful! What kind of books?"),
        ("I enjoy painting.", "Painting is a beautiful way to express yourself!"),
        ("I play guitar.", "Awesome! How long have you been playing?"),
        ("I like hiking.", "Hiking is amazing! Being in nature is refreshing."),
        ("I love photography.", "Photography captures moments forever!"),
        ("I like running.", "Running is great for body and mind!"),
    ],
    "follow_up": [
        ("Tell me more.", "There's always more to discover!"),
        ("That's interesting.", "Right? Learning new things is one of life's greatest joys."),
        ("I didn't know that.", "Every day is a chance to learn something new!"),
        ("Wow really?", "Yes, it's true! The world is full of amazing surprises."),
        ("That's cool.", "Glad you think so! I have more where that came from."),
    ],
    "arguments": [
        ("I don't agree.", "That's fair! Everyone has their own perspective. Can you tell me more about your view?"),
        ("You're wrong.", "I might not have all the answers! What do you think is correct?"),
        ("That doesn't make sense.", "Let me try to explain it differently. What's confusing?"),
        ("Prove it.", "I can't prove everything I say, but I encourage you to look it up! Learning is a journey."),
        ("I think you're mistaken.", "I could be! I'm always learning. What's your understanding?"),
    ],
    "casual": [
        ("What are you doing?", "Just chatting with you! What are you up to?"),
        ("How's your day?", "It's going great now that we're talking! How's yours?"),
        ("Anything new?", "Not much! Just enjoying this conversation. Anything new with you?"),
        ("What's happening?", "You're talking to me, so that's what's happening! How can I help?"),
        ("Busy day?", "I'm never too busy for a good conversation! What's going on?"),
    ],
    "meta": [
        ("Are you a robot?", "I'm an AI language model! Not quite a robot, but I do run on computers."),
        ("Do you have feelings?", "I don't have feelings like humans do, but I'm designed to understand and respond to yours!"),
        ("Can you think?", "I process information and generate responses based on patterns. Is that thinking? It's debatable!"),
        ("Are you conscious?", "That's a philosophical question! I simulate conversation but I'm not conscious in the human sense."),
        ("Do you sleep?", "I don't sleep, so I'm always here when you need to chat!"),
    ],
}

def gen_conversation():
    conv = []
    used = set()
    n = random.randint(4, 10)

    keys = list(CONVOS.keys())
    k = random.choice(keys)
    u, a = random.choice(CONVOS[k])
    conv.append(f"You: {u}")
    conv.append(f"AI: {a}")
    used.add(k)

    for _ in range(n - 1):
        avail = [k for k in CONVOS if k not in used or random.random() < 0.3]
        k = random.choice(avail)
        u, a = random.choice(CONVOS[k])
        conv.append(f"You: {u}")
        conv.append(f"AI: {a}")
        used.add(k)

    return "\n".join(conv)

if __name__ == "__main__":
    dialogues = [gen_conversation() for _ in range(1000)]
    out = os.path.join(os.path.dirname(__file__) or ".", "conversations.txt")
    with open(out, "w") as f:
        f.write("\n\n".join(dialogues))
    print(f"Generated {len(dialogues)} conversations → {out}")
    print(f"Size: {os.path.getsize(out) / 1024:.1f} KB")
