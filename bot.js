const { Client, GatewayIntentBits } = require('discord.js');

const TOKEN = "YOUR_DISCORD_BOT_TOKEN";  // Replace with your bot token
const CHANNEL_ID = "YOUR_CHANNEL_ID";    // Replace with your Discord channel ID

const MESSAGES = [
    "Hey, are we early? 👀",
    "How do I get a role here?",
    "Where’s the roadmap? Need to see what’s cooking. 🔥",
    "Is there a guide on how to start?",
    "What’s the requirement to be eligible?",
    "Did I miss it, or is it still open?",
    "When’s the next update?",
    "What’s next after this?",
    "Who’s been here the longest?",
    "How do I check my status?",
    "Is there a way to track progress?",
    "Can someone drop a step-by-step guide?",
    "What’s the best way to stay updated?",
    "Any perks for early members?",
    "How do I invite friends to join?",
    "What’s the official announcement channel?",
    "Who do I contact if I have issues?",
    "Is there a way to verify my account?",
    "How do I know if I’m in?",
    "What’s the timeline for this?",
    "Where can I find the full details?",
    "What’s the easiest way to get started?",
    "Is there a checklist of things to do?",
    "What’s the next step after signing up?",
    "Are there different levels or tiers?",
    "How do I know if I completed all the steps?",
    "Is there a leaderboard or ranking?",
    "What’s the most important thing to do right now?",
    "Can someone confirm if everything is working fine?",
    "What’s the most common mistake people make here?"
];

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages]
});

client.once('ready', () => {
    console.log(`✅ Bot logged in as ${client.user.tag}`);

    setInterval(() => {
        const channel = client.channels.cache.get(CHANNEL_ID);
        if (channel) {
            const message = MESSAGES[Math.floor(Math.random() * MESSAGES.length)];
            channel.send(message).then(() => {
                console.log(`📩 Sent: "${message}"`);
            }).catch(err => console.error(`❌ Error sending message: ${err}`));
        } else {
            console.error("❌ Channel not found!");
        }
    }, 30000); // Sends a message every 30 seconds
});

client.login(TOKEN);
