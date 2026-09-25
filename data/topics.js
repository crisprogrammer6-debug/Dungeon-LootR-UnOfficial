/**
 * Events and NPC's topic boards.
 */
window.TOPICS = {
  events: [
    {
      id: "payload",
      title: "Payload",
      image: "assets/img/events/PayloadEvent.png?v=1",
      extra: ["assets/img/events/PayloadEventShop.png?v=1"],
      info: `<p>Payload is an island-hopping wave event. You need <strong>level 40+</strong> just to enter the lobby, but that is only the door — each difficulty has its own level gate on top of that.</p>
        <p>You fight across a chain of islands. Each island throws a pair of enemy waves at you. Clear them and you get chests plus short-term buffs before you move on. You are not always solo: NPCs can drop in and fight alongside you.</p>
        <p>The last island is a boss fight against <strong>Torus</strong>.</p>
        <h3>Difficulties</h3>
        <ul>
          <li>Easy — Level 40+</li>
          <li>Normal — Level 75+</li>
          <li>Hard — Level 100+</li>
          <li>Nightmare — Level 150+</li>
        </ul>
        <h3>Rewards</h3>
        <p>A clear pays out materials and equipment, plus <strong>Aether Marks</strong> — the event coin. Spend Marks at the Payload Shop on the lobby boat for event stock (classes, titles, gear, and more). Daily shop stock resets at midnight UTC.</p>`,
    },
    {
      id: "magic-unleashed",
      title: "Magic Unleashed",
      image: "assets/img/events/MagicUnleashedEvent.png?v=22",
      extra: ["assets/img/events/MagicUnleashedEventShop.png?v=19"],
      info: `<p>Magic Unleashed is a high-end raid boss — a hard clear, not a farm loop. Bring a real setup, learn the fight, and push for the kill. Clears pay out event cosmetics, event equipment, Mage Coins, and a mix of other drops. Mage Coins are the event currency: spend them in the Magic Unleashed shop on event gear, event cosmetics, event chests, plus a handful of base-game items. If you are chasing the full event look, this shop is the main sink.</p>`,
    },
    {
      id: "tournament",
      title: "Tournament",
      image: "assets/img/events/TournamentEvent.png?v=22",
      extra: ["assets/img/events/TournamentUI.png?v=22"],
      info: `<p>Tournament is a timed damage race. Dump as much damage as you can before the clock hits zero. A big number is nice — a leaderboard seat is the actual win.</p>
        <h3>Requirements</h3>
        <p>Record the full run. Staff will not lock in podium placements or pay out rewards without footage they can review.</p>
        <h3>Modes</h3>
        <p>Solo and Duo are both live. Pick the lane that fits your roster.</p>
        <h3>Modifiers</h3>
        <p>Every two weeks the lobby rotates a new package of buffs and debuffs. They hit both players and enemies, so the fight — and the meta — shifts each cycle.</p>
        <h3>Tournament rules</h3>
        <ol class="event-rules">
          <li>Final leaderboard placements are subject to staff review. Rewards drop after staff approval, or three days after the season ends if the placement is still unreviewed. Denied rewards do not unlock after that window.</li>
          <li>Do not use exploits, abuse bugs, or lean on unintended mechanics for an unfair edge. Dungeon LootR staff decide whether a run breaks this rule.</li>
          <li>Staff may deny leaderboard rewards if a review finds cheating, unfair play, or Tournament / game-rule violations. A board placement does not guarantee payout.</li>
          <li>Do not bypass Tournament entry locks — including moderation-flag lockouts — with alts, bugs, or other workarounds. Doing so can void your leaderboard rewards.</li>
          <li>By entering, you agree that authorized Dungeon LootR staff may review your in-game player data to check eligibility and rule compliance.</li>
          <li>If your lifetime moderation-flag total goes over 100 before the season’s three-day review period ends, you forfeit that season’s placement and rewards, even if you earned the seat first.</li>
          <li>Play honest. Do not hunt loopholes in these rules to steal an advantage or dodge restrictions.</li>
        </ol>`,
    },
  ],
  npcs: [
    {
      id: "group-reward",
      title: "Group Reward",
      image: "assets/img/npcs/GroupRewardNPC.png?v=19",
      info: "Pays out rewards for joining the group.",
    },
    {
      id: "limited-emotes",
      title: "Limited Emotes",
      image: "assets/img/npcs/LimitedEmotesNPC.png?v=19",
      info: "A Robux emote shop. The stock rotates over time.",
    },
    {
      id: "challenge-guide",
      title: "Challenge Guide",
      image: "assets/img/npcs/ChallengeGuideNPC.png?v=19",
      info: "Covers Challenges: what they are and what they pay, just an info NPC.",
    },
    {
      id: "forge-guide",
      title: "Forge Guide",
      image: "assets/img/npcs/ForgeGuideNPC.png?v=19",
      info: "Breaks down the Forge — what it does, why it matters, and what it needs to run.",
    },
    {
      id: "artemis",
      title: "Artemis",
      image: "assets/img/npcs/ArtemisNPC.png?v=19",
      info: "Talk to claim the God Hunter title by taking the Artemis class to Mastery 50.",
    },
    {
      id: "cursed-king",
      title: "Cursed King",
      image: "assets/img/npcs/CursedKingNPC.png?v=19",
      info: "Talk to claim the King of Curses title. Cost: 1M coins plus King of Curses at Mastery 50.",
    },
    {
      id: "hitman-aura-farmer",
      title: "Hitman & Aura Farmer",
      image: "assets/img/npcs/HitmanAuraFarmerNPC.png?v=19",
      info: "Currently no listed gameplay role or rewards.",
    },
    {
      id: "guide",
      title: "Guide",
      image: "assets/img/npcs/GuideNPC.png?v=19",
      info: "Walks you through the basics — a short onboarding tutorial that gets you moving in Dungeon LootR.",
    },
    {
      id: "genesis",
      title: "Genesis",
      image: "assets/img/npcs/GenesisNPC.png?v=1",
      info: "Currently no listed class quest or reward.",
    },
    {
      id: "forge-archon",
      title: "Forge Archon",
      image: "assets/img/npcs/ForgeArchonNPC.png?v=19",
      info: "Talk to claim the Infinite Blade Works title. Requirements: Forge Archon at Mastery 50 and 1M coins.",
    },
    {
      id: "mystery-merchant",
      title: "Mystery Merchant",
      image: "assets/img/npcs/MysteryMerchantNPC.png?v=19",
      info: "A traveling shop that appears every two hours and stays for 15 minutes. Everything here is bought with Stars.",
    },
    {
      id: "great-mage",
      title: "Great Mage",
      image: "assets/img/npcs/GreatMageNPC.png?v=19",
      info: "Tells you how to obtain Demonbane (Battle Pass tier 50) and offers a title quest: 1M coins plus Demonbane at Mastery 50.",
    },
    {
      id: "devil-hunter",
      title: "Devil Hunter",
      image: "assets/img/npcs/DevilHunterNPC.png?v=19",
      info: "Talk to claim the Devil Hunter title. Requirements: Sinister Triggers at Mastery 50, 2M coins, 5 Devil Hunter, and 2 Exotic Ingots.",
    },
    {
      id: "afk",
      title: "AFK",
      image: "assets/img/npcs/AFKNPC.png?v=19",
      info: "Sends you to the AFK world. Without Premium or passes, rewards tick every 20 minutes. The server force-rejoins you every 16 minutes so you are not kicked.",
    },
    {
      id: "kage",
      title: "Kage",
      image: "assets/img/npcs/KageNPC.png?v=1",
      info: `<p>This NPC offers the quest for the Black Falcon title, claimed through Kage mastery and a tribute of coin.</p>
        <p><strong>Requirements:</strong> Kage Mastery 50 + 1,000,000 coins.<br>
        <strong>Awards:</strong> Title "Black Falcon".</p>`,
    },
    {
      id: "unrestricted-fighter",
      title: "Unrestricted Fighter",
      image: "assets/img/npcs/UnrestrictedFighterNPC.png?v=1",
      info: `<p>Turn in Heavenly Fragments here to forge the Inverted Spear — the class item that transforms the wielder into Unrestricted.</p>
        <p><strong>Requirements:</strong> Honored One Mastery 25 + 1,000,000 coins.<br>
        <strong>Awards:</strong> Inverted Spear.</p>`,
    },
    {
      id: "valen",
      title: "Valen",
      image: "assets/img/npcs/ValenNPC.png?v=1",
      info: `<p>Completing this NPC's quest grants Awakened Devil EX. Devil Hearts from the Awakened Devil on Frostspire (Nightmare+) are turned in here and at Jetstream.</p>
        <p><strong>Requirements:</strong> Azure Devil Mastery 50 + 1 Devil Heart + 500,000 coins.<br>
        <strong>Awards:</strong> Judgements Edge.</p>`,
    },
    {
      id: "jetstream",
      title: "Jetstream",
      image: "assets/img/npcs/JetstreamNPC.png?v=1",
      info: `<p>Completing this NPC's quest grants the Jetstream class. Devil Hearts from the Awakened Devil on Frostspire (Nightmare+) are turned in here and at Valen.</p>
        <p><strong>Requirements:</strong> Azure Devil Mastery 50 + 3 Devil Hearts + Exotic Shattered Armor + 200,000 coins.<br>
        <strong>Awards:</strong> Cybernetic Katana.</p>`,
    },
    {
      id: "the-dev",
      title: "The Dev",
      image: "assets/img/npcs/TheDevNPC.png?v=1",
      wide: true,
      info: `<p class="npc-dev-intro">This NPC stands as a monument to the creator and owner of Dungeon LootR — a living tribute to the architect who forged this world.</p>
        <p class="npc-dev-quote">Thanks everyone for having played my game. This game was ~3 years in the making; achieving more than I could have ever dreamed of achieving. I've brought my family out of debt, created a future career for myself, and proved myself wrong in every way possible. No matter the future of this game, thank you all for having played.</p>`,
    },
  ],
};
