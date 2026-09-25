/**
 * Dungeon LootR — Class Tier List
 * Edit this file to add, move, or restyle classes.
 *
 * Tiers: change `TIERS` order, label, or color.
 * Classes: add an object to `CLASSES`.
 * Rarities / archetypes: add keys to `RARITIES` / `ARCHETYPES`.
 */

window.LOOTR = {
  meta: {
    title: "CLASS TIER LIST",
    game: "Dungeon LootR",
    source: "Information from Cristian, owner of this page.",
    version: "Season snapshot",
  },

  TIERS: [
    { id: "meta", label: "META", rank: "01", note: "Current competitive standard." },
    { id: "s", label: "S", rank: "02", note: "High ceiling. First-line viable." },
    { id: "a", label: "A", rank: "03", note: "Strong. Requires correct execution." },
    { id: "b", label: "B", rank: "04", note: "Playable. Situation-dependent." },
    { id: "d", label: "D", rank: "05", note: "Limited role. Outclassed in most content." },
    { id: "f", label: "F", rank: "06", note: "Not recommended for current meta." },
  ],

  RARITIES: {
    rare: { label: "Rare", hex: "#3b82f6" },
    epic: { label: "Epic", hex: "#8b5cf6" },
    legendary: { label: "Legendary", hex: "#d4a017" },
    mythic: { label: "Mythic", hex: "#ef4444" },
    celestial: { label: "Celestial", hex: "#22d3ee" },
    exotic: { label: "Exotic", hex: "#f472b6" },
  },

  ARCHETYPES: {
    tempest: { label: "Tempest", icon: "assets/img/tempest.png?v=17" },
    aegis: { label: "Aegis", icon: "assets/img/aegis.png?v=17" },
    ruin: { label: "Ruin", icon: "assets/img/ruin.png?v=17" },
    umbral: { label: "Umbral", icon: "assets/img/umbral.png?v=17" },
    alacrity: { label: "Alacrity", icon: "assets/img/alacrity.png?v=17" },
    fulmin: { label: "Fulmin", icon: "assets/img/fulmin.png?v=17" },
  },

  /**
   * Podiums: Magic (crest), Ranged (bow), Physical (shield).
   */
  MARKS: [
    {
      id: "magic",
      label: "Magic",
      icon: "assets/img/tempest.png?v=17",
      archetypes: ["tempest"],
    },
    {
      id: "ranged",
      label: "Ranged",
      icon: "assets/img/ruin.png?v=17",
      archetypes: ["ruin", "umbral"],
    },
    {
      id: "physical",
      label: "Physical",
      icon: "assets/img/aegis.png?v=17",
      archetypes: ["aegis", "alacrity", "fulmin"],
    },
  ],

  CLASSES: [
    { name: "Draconia", tier: "meta", rarity: "exotic", archetype: "tempest", isNew: true },
    { name: "Dark Professor", tier: "meta", rarity: "exotic", archetype: "tempest" },
    { name: "Dragoon", tier: "meta", rarity: "exotic", archetype: "tempest" },
    { name: "Fae", tier: "meta", rarity: "exotic", archetype: "tempest", isNew: true },
    { name: "Hellfiend", tier: "meta", rarity: "exotic", archetype: "tempest" },

    { name: "Crescent Blade", tier: "s", rarity: "exotic", archetype: "ruin", isNew: true },
    { name: "Embertide", tier: "s", rarity: "exotic", archetype: "tempest" },
    { name: "Unrestricted", tier: "s", rarity: "celestial", archetype: "aegis" },
    { name: "Dreadlord", tier: "s", rarity: "exotic", archetype: "aegis" },
    { name: "Coyote", tier: "s", rarity: "exotic", archetype: "tempest" },
    { name: "Shadow Vagrant", tier: "s", rarity: "exotic", archetype: "tempest" },
    { name: "Sinister Trigger", tier: "s", rarity: "exotic", archetype: "ruin" },
    { name: "Cryomancer", tier: "s", rarity: "exotic", archetype: "tempest" },
    { name: "Moon Witch", tier: "s", rarity: "celestial", archetype: "tempest", isNew: true },
    { name: "Spell Breaker", tier: "s", rarity: "exotic", archetype: "tempest" },
    { name: "Anti Magic", tier: "s", rarity: "exotic", archetype: "tempest" },
    { name: "Awakened Devil EX", tier: "s", rarity: "exotic", archetype: "ruin" },
    { name: "Jetstream", tier: "s", rarity: "exotic", archetype: "tempest" },

    { name: "Zero", tier: "a", rarity: "exotic", archetype: "tempest" },
    { name: "Founder", tier: "a", rarity: "exotic", archetype: "tempest" },
    { name: "Frame Breaker", tier: "a", rarity: "exotic", archetype: "tempest" },
    { name: "Chaotic Fist", tier: "a", rarity: "exotic", archetype: "tempest" },
    { name: "Honored One", tier: "a", rarity: "exotic", archetype: "tempest" },
    { name: "Azure Devil", tier: "a", rarity: "celestial", archetype: "alacrity" },
    { name: "Demonbane", tier: "a", rarity: "celestial", archetype: "tempest" },
    { name: "Necromancer", tier: "a", rarity: "celestial", archetype: "ruin", isNew: true },

    { name: "Vacio", tier: "b", rarity: "celestial", archetype: "tempest" },
    { name: "Artemis", tier: "b", rarity: "celestial", archetype: "umbral" },
    { name: "Cursed King", tier: "b", rarity: "exotic", archetype: "tempest" },
    { name: "Kage", tier: "b", rarity: "legendary", archetype: "tempest" },
    { name: "Witch Gunner", tier: "b", rarity: "legendary", archetype: "ruin" },
    { name: "Boxer", tier: "b", rarity: "epic", archetype: "aegis" },

    { name: "Cursed Child", tier: "d", rarity: "mythic", archetype: "fulmin" },
    { name: "Divergent", tier: "d", rarity: "mythic", archetype: "fulmin" },
    { name: "Wanderer", tier: "d", rarity: "mythic", archetype: "fulmin" },
    { name: "Forge Archon", tier: "d", rarity: "celestial", archetype: "tempest" },

    { name: "Archer", tier: "f", rarity: "legendary", archetype: "umbral" },
    { name: "Shinobi", tier: "f", rarity: "legendary", archetype: "fulmin" },
    { name: "Assassin", tier: "f", rarity: "epic", archetype: "fulmin" },
    { name: "Flame Bastion", tier: "f", rarity: "epic", archetype: "fulmin" },
    { name: "Bowman", tier: "f", rarity: "rare", archetype: "fulmin" },
    { name: "Greatsword", tier: "f", rarity: "rare", archetype: "fulmin" },
    { name: "Ronin", tier: "f", rarity: "rare", archetype: "fulmin" },
  ],
};
