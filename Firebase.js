import {initializeApp} from "firebase/app";            //firebase
import {getFirestore} from 'firebase/firestore';        //firestore
import { getStorage, ref } from "firebase/storage";     //storage
import { collection, doc, setDoc } from "firebase/firestore"; 
import { collection, addDoc } from "firebase/firestore"; 
import { doc, updateDoc,increment } from "firebase/firestore";
import { doc, deleteDoc } from "firebase/firestore";
import { collection, query, where, getDocs } from "firebase/firestore";
// Get a reference to the storage service, which is used to create references in your storage bucket


// Create a storage reference from our storage service
//const storageRef = ref(storage);


const firebaseConfig = {
    apiKey: "AIzaSyCFM5p5mDUEGNBq0dtdyV6dG6mp6TJdIRY",
    authDomain: "ba-automation-5a4ae.firebaseapp.com",
    databaseURL: "https://ba-automation-5a4ae-default-rtdb.firebaseio.com",
    projectId: "ba-automation-5a4ae",
    storageBucket: "ba-automation-5a4ae.appspot.com",
    messagingSenderId: "60846272657",
    appId: "1:60846272657:web:16281e82c4df5b8721cf30"
  };
  
  // Initialize Firebase
  export const app = initializeApp(firebaseConfig);
  export const database =getFirestore(app);
  export const storage =getStorage(app);

 
  


const storage = getStorage();

// Points to the root reference
const storageRef = ref(storage);

// Points to 'images'
const imagesRef = ref(storageRef, 'images');

// Points to 'images/space.jpg'
// Note that you can use variables to create child values
const fileName = 'space.jpg';
const spaceRef = ref(imagesRef, fileName);

// File path is 'images/space.jpg'
const path = spaceRef.fullPath;

// File name is 'space.jpg'
const name = spaceRef.name;

// Points to 'images'
const imagesRefAgain = spaceRef.parent;

///////////////////////////////////////////////////////////////////////////////////////////////


$(document).ready(function() {

  //initiate dp
  var dp=firebase.firestore();
 //read data entered
 $("button").click(function(e) {
e.preventDefault();
  var user_contnt=$("button").val();
  dp.collection("#users").add[(userInfo :Name)].then((docRef))=>
 });
});


//////////////////////////////////////////////////////////////////////////////////////////////////
$(document).ready(function() {
  //SIGN UP FUNCTION----
// just save data
  // Add a new document in collection "users" (UserInfo1)
await setDoc(doc(db, "users", "UserInfo1"), {
  Name: "mariam",
  Email: "mariam123",
  Password: "CA",
  Role: "ba",
  ID: "98",
});
// const li = document.querySelector("button")
// $("button").click(()=>{
//   dafdsf ss
// })
// Add a new document with an auto generated id.

const new_document_reference1 = doc(collection(db, "users"), {
  Name: "kero",
  Email: "kero123",
  Password: "123",
  Role: "ba",
  ID: "67",
});
await setDoc(new_document_reference1, data);


// print
console.log("Document written with ID: ", docRef.id);

// add new project for the registerd user FUNCTION
// Add a new document in collection "Projects" WITH SAVED REFERENCE AND GENRATED ID
const new_document_reference = doc(collection(db, "Projects"), {
  Name: "web app",
  Description: "SHOES WBSITE",
  Docs: "REFERENCE FROM STORAGE",
  ID: new_document_reference,  // REFERENCE OF DOCUMENT
  userID: currunt_id,
});
await setDoc(new_document_reference, data);



// update functions for user

const newRef = doc(db, "users", "UserInfo1");

await updateDoc(newRef, {
  Name: "kero",
  Email: "kero123",
  Password: "123",
  Role: "ba",
  ID: "67",
});

// update functions for projects
const newRef1 = doc(db, "Projects", new_created_projecr);
await updateDoc(new_created_projecr, {
  Name: "web app",
  Description: "SHOES WBSITE",
  Docs: "REFERENCE FROM STORAGE",
  
});
//DELETE PROJECT FUNCTION 
await deleteDoc(doc(db, "Projects", new_created_projecr));

//GET PROJECTS OF A USER
const q = query(collection(db, "Projects"), where("userID", "==", currunt_id));

const querySnapshot = await getDocs(q);
querySnapshot.forEach((doc) => {
  // doc.data() is never undefined for query doc snapshots
  console.log(doc.id, " => ", doc.data());
});


});
