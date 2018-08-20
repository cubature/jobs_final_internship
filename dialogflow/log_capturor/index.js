// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');

// configuration of database
var admin = require('firebase-admin');

admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  databaseURL: 'https://collaborateuragence.firebaseio.com'
});

var db = admin.database();
var ref = db.ref();

ref.orderByChild("timestamp").on("value", function(snapshot) {
  console.log(snapshot.val());
});

// treatments of giving the response to dialogflow
process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function welcome(agent) {
    agent.add(`Welcome to my agent!`);
  }
 
  function fallback(agent) {
    console.log(`La question ne peut pas être résolue: ` + agent.query);
    agent.add(`J'ai du mal à comprendre cette question. (avec humour)`);
    ref.push().set({
      "question": agent.query,
      "timestamp": new Date().toISOString()
    });
}

   // Uncomment and edit to make your own intent handler
   // uncomment `intentMap.set('your intent name here', yourFunctionHandler);`
   // below to get this function to be run when a Dialogflow intent is matched
  function Conges_information(agent) {
     agent.add(`😁Vous pouvez les trouver sur ce ligne dans la rubrique Absences`);
     agent.add(new Card({
         title: `MyConnect😁`,
         imageUrl: 'https://www.niort-numeric.fr/wp-content/uploads/2017/02/sogeti-logo2.jpg',
         text: `MyConnect😁`,
         buttonText: 'Entre😁',
         buttonUrl: 'https://myhr-capgemini.neocaseonline.com/Default.aspx'
      })
     );
     agent.add(new Suggestion(`Merci 😁`));
     agent.add(new Suggestion(`OK😁`));
     //agent.setContext({ name: 'weather', lifespan: 2, parameters: { city: 'Rome' }});
  }
  function Conges_type(agent) {
     agent.add(`Il y a les congés spéciaux (sabbatique, création d’entreprise, sans solde, ...), les congés légaux (CP, CPA), les congés spéciaux pour raisons familiales, les congés maternité, les congés adoption. Vous pouvez trouver les informations complémentaires sur ce ligne dans la rubrique Absences.`);
     agent.add(new Card({
         title: `MyConnect`,
         imageUrl: 'https://pbs.twimg.com/profile_images/458977970716024832/_mOFbecc_400x400.png',
         text: `MyConnect`,
         buttonText: 'ENTRE',
         buttonUrl: 'https://myhr-capgemini.neocaseonline.com/Default.aspx'
      })
     );
     agent.add(new Suggestion(`Merci`));
     agent.add(new Suggestion(`OK`));
     //agent.setContext({ name: 'weather', lifespan: 2, parameters: { city: 'Rome' }});
  }

   // Uncomment and edit to make your own Google Assistant intent handler
   // uncomment `intentMap.set('your intent name here', googleAssistantHandler);`
   // below to get this function to be run when a Dialogflow intent is matched
  function googleAssistantHandler(agent) {
     let conv = agent.conv(); // Get Actions on Google library conv instance
     conv.ask('Hello from the Actions on Google client library!') // Use Actions on Google library
     agent.add(conv); // Add Actions on Google library responses to your agent's response
  }
   // See https://github.com/dialogflow/dialogflow-fulfillment-nodejs/tree/master/samples/actions-on-google
  // // for a complete Dialogflow fulfillment library Actions on Google client library v2 integration sample

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('Conges information', Conges_information);
  intentMap.set('Conges types', Conges_type);
//intentMap.set('your intent name here', googleAssistantHandler);
  agent.handleRequest(intentMap);
});