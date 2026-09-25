/**
 * Browser posts here. The Discord webhook lives only on the relay
 * (tools/suggestions-bot.py), never in this file.
 */
window.SUGGESTIONS = {
  endpoint: "http://127.0.0.1:5182/suggest",
};
