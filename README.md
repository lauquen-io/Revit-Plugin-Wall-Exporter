# PyRevit export json

This is a custon plug in made with PyRevit. The objective of this repo is to have a plug in that transforms individualy each of the basic walls on the document to an array of vertices. 

The vertices are expressed in the form of X and Y cooridinates. The width of the wall is not taken in consideration.

The program will save a file on the path of the document you are working on. The file will contain the mark of each individual wall and the array of vertices in the form of:

{
    "name": "01-09", 
    "points": [
      {
        "y": 0, 
        "x": 0
      }, 
      {
        "y": 0, 
        "x": 1220.0
      }, 
      {
        "y": 1428.0, 
        "x": 1220.0
      }, 
      {
        "y": 2440.0, 
        "x": 0.0
      }
    ]
  }
 
