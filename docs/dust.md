Dustage GCS
========


Introduction
------------

Dustage is a GCS heavily inspired by __MegaZeux__.



Layers
------

Every object you interact with in Dust, save for __offscreen Actors__, is placed on a Layer.  Layers are flexible, movable, resizable planes upon which you can put graphics, built-in objects, and Actors.  There are two types of Layers:  Graphics layers and Game layers.

Layers are ideal for any sort of graphical effects, like clouds over top of your world, a text box with text, a particle engine that splatters things, a heads-up display, stars in a chasm beneath your precarious level, or many other things.  By stacking layers, you can create a layer that represents a ship flying above passing stars and behind planets, an underwater cavern with mottled wave light patterns flickering across the sea floor, a thick forest with foliage spanning above the overgrown paths and leaves slowly spiraling to the forest floor, a winter landscape with snowflakes lazily drifting down to the ground, or anything else that you want, with interactive elements that the Player and Actors can move, affect, and be affected by.


Actors: What They Are and How to Use Them
-----------------------------------------

When you think of an actor, you may think of a talented movie star, a performer in a play, or a dramatic ham in a soap opera.  Actors in Dustage can be all of these things and more.  Actors can be *"on stage"* where they shine on a Layer, or they work behind the scenes when placed *"off stage."*  All Actors, of course, must have a __Script__, a set of instructions that tells the Actor what to do.  Scripts look something like this:

| An Example Script          | What It Does                          |
| -------------------------- | ------------------------------------- |
| __when__ __adjacent__      | When the player steps next to me...   |
| __say__ "Come closer..."   | Beckon them closer...                 |
| __return__                 | And go back to what I was doing.      |
| __when__ __touched__       | When the player presses towards me... |
| __say__ "Why hello there!" | Greet them...                         |
| __return__                 | And go back to what I was doing.      |



File Format
-----------

### Structure

Dustage projects are stored in a ~~deflated~~ JSON format.

Here is an example of a bare minimum world with defaults for new objects (with an Actor added in just for example's sake):

```javascript
{
  "name": "New World",
  "counters": {},
  "actors": [],
  "layers": [],
  "boards": [
    {
      "w": 80,
      "h": 25,
      "x": 0,
      "y": 0,
      "name": "New Board",
      "counters": {},
      "actors": [],
      "layers": [
        {
          "w": 80,
          "h": 25,
          "x": 0,
          "y": 0,
          "name": "New Layer",
          "gamemap": [
            [
              1, // ID (1 = Space)
              7, // Color (7 = Default Light Gray)
              0  // Parameter
            ]
          ],
          "actors": [
            {
              "name": "New Actor",
              "w": 1,
              "h": 1,
              "x": 0,
              "y": 0,
              "counters": {},
              "script": ""
            }
          ]
        }
      ]
    }
  ]
}```

### Object Property Table

Object | Property  | Type         | Default       | Description
------ | --------  | :----------: | :------------ | :---
World  | `name`    | String       | `"New World"` | A brief name for the World.
World  | `counters`| Object       | `{}`          | _Local counters_; key-value pairs representing World-wide counters.
World  | `actors`  | List         | `[]`          | _Global Offscreen Actors_.  List of Actor objects that are global.
World  | `layers`  | List         | `[]`          | _Global Layers_.  List of Layer objects that are present on all Boards.
World  | `boards`  | List         | `[]`          | List of Boards in the World.  By default, each World's `boards` contains a default Board.
Board  | `name`    | String       | `"New Board"` | A brief name for the Board.
Board  | `w`       | Integer      | `100`         | Width of the board, in tiles.
Board  | `h`       | Integer      | `100`         | Height of the board, in tiles.
Board  | `counters`| Object       | `{}`          | _Local counters_; key-value pairs representing Board-specific counters.
Board  | `actors`  | List         | `[]`          | _Local Offscreen Actors_.  List of Actor objects that are on the board but offscreen.
Board  | `layers`  | List         | `[]`          | List of Layer objects on this board.  By default, each Board's `layers` contains a default Layer.
Layer  | `name`    | String       | `"New Layer"` | A brief name for the Layer.
Layer  | `w`       | Integer      | `100`         | Width of the Layer, in tiles.
Layer  | `h`       | Integer      | `100`         | Height of the Layer, in tiles.
Layer  | `x`       | Integer      | `0`           | X offset of the board, in tiles.
Layer  | `y`       | Integer      | `0`           | Y offset of the board, in tiles.
Layer  | `sprite`  | Object       | `{}`          | Graphical Map representing the layer's graphical contents.
Layer  | `actors`  | List         | `[]`          | List of Actor objects that are visible on the Layer.
Actor  | `name`    | String       | `"New Actor"` | A brief name for the Actor.
Actor  | `w`       | Integer      | `1`           | Height of the Actor, in tiles.
Actor  | `h`       | Integer      | `1`           | Width of the Actor, in tiles.
Actor  | `x`       | Integer      | `0`           | X position of the Actor on its Layer, in tiles.
Actor  | `y`       | Integer      | `0`           | Y position of the Actor on its Layer, in tiles.
Actor  | `counters`| Object       | `{}`          | _Actor counters_; key-value pairs representing Board-specific counters.
Actor  | `script`  | String       | `""`          | The Actor's Script.
Layer  | `sprite`  | Object       | `{}`          | Graphical Map representing the layer's graphical contents.
Sprite | `w`       | Integer      | `1`           | Height of the graphical map, in tiles.
Sprite | `h`       | Integer      | `1`           | Width of the graphical map, in tiles.
Sprite | `x`       | Integer      | `0`           | X position of the Actor on its Layer, in tiles.
Sprite | `y`       | Integer      | `0`           | Y position of the Actor on its Layer, in tiles.
Sprite | `tilemap` | List         | `[]`          | List of Integers representing a single ASCII char.  Should be `w*h` items long.

Glossary
--------

##### Actor
An **Actor** is an object that commonly resides on a Layer.
