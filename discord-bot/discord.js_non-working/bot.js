var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
var pingReplyMessages = ["Eat shit, peasant.", "I will cut you.", "Kill yourself", "Nobody loves you"];
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ');
    logger.info(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`
    if (message.substring(0, 1) == '!') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
        var opt0 = args[1];
        var opt1 = args[2];

        if (opt0 != null) {
          if (opt0.substring(0, 1) == '<') {
            var uid = opt0.slice(3, 21);
          }
        }
        if (opt1 != null) {
          if (opt1.substring(0, 1) == '<') {
            var uid = opt1.slice(3, 21);
          }
        }
        args = args.splice(1);
        //var targetUid = opt0.toString();
        logger.info('User: ' + user);
        logger.info('uid: ' + userID);
        logger.info('Opt0: ' + opt0);
        logger.info('Opt1: ' + opt1);
        switch(cmd) {
            // !ping
            case 'ping':
                bot.sendMessage({
                    to: channelID,
                    message: pingReplyMessages[Math.floor(Math.random()*5)]
                });
            break;

            case 'getuid':
              if (opt0 == null) {
                bot.sendMessage({
                  to: channelID,
                  message: userID
                });
              }
              else {
                bot.sendMessage({
                  to: channelID,
                  message: uid
                });
              }

            break;

            case 'kick':
                bot.kick({
                  target: uid
                });
                bot.sendMessage({
                    to: channelID,
                    message: 'User ' + uid + ' kicked'
                });
                logger.info('uid: ' + uid + ' kicked from server');
            break
            // Just add any case commands if you want to..
         }
     }
});
