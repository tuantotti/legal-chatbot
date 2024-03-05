/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'legal-chatbot';
const collection = 'law-collection';
const collection_test = 'law-collection-test';

// Create a new database.
use(database);

// Create a new collection.

db.createCollection(collection, {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["lawId", "newsCode", "articles", "content"],
         properties: {
            lawId: {
               bsonType: "int"
            },
            newsCode: {
              bsonType: "string"
            },
            articles: {
               bsonType: "array"
            },
            content: {
              bsonType: "string"
            },
         }
      }
   }
})

// Tạo index cho trường lawId
db.collection.createIndex({ "lawId": 1 })

// Tạo collection với hai trường lawId và articles
db.createCollection(collection_test, {
  validator: {
     $jsonSchema: {
        bsonType: "object",
        required: ["lawId", "newsCode", "articles", "content"],
        properties: {
           lawId: {
              bsonType: "int"
           },
           newsCode: {
             bsonType: "string"
           },
           articles: {
              bsonType: "array"
           },
           content: {
             bsonType: "string"
           },
        }
     }
  }
})

// Tạo index cho trường lawId
db.collection_test.createIndex({ "lawId": 1 })


// More information on the `createCollection` command can be found at:
// https://www.mongodb.com/docs/manual/reference/method/db.createCollection/