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



### Actor Syntax

Most lines take the form `command argument` where argument can be a variable, expression, number, string, or nested command.

#### Helping Words

Helping words allow the language to flow more smoothly.

##### `is`, `am`, `are`

These commands allow you to pass arguments to a command before a function.  For example, you could use `if blocked forward player` to check if an actor named _Player_ is blocked in the _forward_ direction.  However, a more natural way to write this would be `if player is blocked forward`.  This is processed in the same way as `if blocked forward player`.

The words `is`, `am` and `are` are completely interchangeable, but of course, some sound gramatically better than others.  This is meant to prevent constructs like `if i is blocked`, which doesn't sound the best.

##### `'s`

The 's command is similar to `is` in that it references another object instead of the default Actor (usually `me`).  However, it will instead reference an Actor's property, if it exists.

##### `my`

Equivalent to saying `me's`.  You can probably guess that this exists because of how much better `my` sounds when compared to `me's`.

### Actor Commands

#### List of commands

##### `backward`

The direction opposite where the Actor is pointing.  Equivalent to `opp`.  See __Directions__, __Point__, __Forward__.  For __offscreen Actors__, this is always equal to `south`.

##### `blocked`

Checks to see if the actor collides with something if it were to move forward.  You can supply a direction, i.e. `blocked north`, to check for a specific direction.  You can also use `is` to supply a different Actor to check, i.e., `player is blocked forward`.

##### `clockwise`

Returns the direction clockwise of the current Actor's heading.  You can supply a direction to `clockwise`; for example `clockwise north` is equal to `east`.  You can also supply an actor to be relative from, i.e. `clockwise (forward of player)` or just `clockwise player` (both are equal).

##### `close file`

Closes an open file object.  See __Open file__.

##### `counterclockwise`

The direction 90 degrees counterclockwise of the Actor's heading.  Equivalent to `opp clockwise`.  You can supply a direction to `counterclockwise`; for example `counterclockwise north` is equal to `west`.  You can also supply an actor to be relative from, i.e. `counterclockwise (player's forward)` or just `counterclockwise player` (both are equal).

##### `for each`

Loop over `it`.  This command can be given an argument to use something other than `it` to loop over.  If the argument is a number, it runs once.  If the argument is a string, it iterates over each character as a number.  If the object is a list, it runs once for each item in the list.  In each loop, `it` will be set to the argument or piece of the argument in question, and `index` will be set to the index of the argument in question.

##### `forward`

The direction that the Actor is facing.  It can be given a reference to an Actor to use that Actor's heading, i.e. `forward player`.  For __offscreen Actors__, this is always equal to `north`. ~~Needs to be equivalent to some inherent property of onscreen Actors.~~

##### `go`

Moves the Actor forward one step.  It can be given a direction argument.  See __Forward__.

##### `goto`

Makes the Actor jump to the given command.  This does not have to be a label.

##### `if`

Conditional statement.  (More)

##### `jump`

Makes the Actor jump to the given label.  You can supply another Actor as an argument to make them jump instead; for example, `jump robert to start`.

##### `length`

Returns the length of the argument.  If the argument is a number, it returns the number of digits in the number.

##### `loop`

Conditional statement that creates a loop that can only be exited by `goto` or `jump` or by recieving a `trigger` command.

##### `open file`

Opens a file for writing; takes an argument that must be a string pointing to a file name.  You will want to set something to the result of `open file` so you can use it later.  For example, you can do `open file "mars.txt"` and then, on the next line, `set mars_data to that`.

##### `opp`

Returns the direction opposite of the Actor's heading.  If an argument is given, it returns the opposite of that.  For example, `opp north` is equal to `south`.  See also __backward__.

##### `point`

Makes the Actor face in the given direction.  Takes a direction as an argument.  It can also take the name of another Actor as an argument; for example, `point Lewis to west` or `point curly backward`.

##### `print`

Prints out the variable in a representative format.  See also __say__.

##### `prompt`

Prompts the user for a variable of a given type.  It can take a variable type as an argument, such as `prompt number` or `prompt string`.  Best used with the `say` command.

##### `say`

Equivalent to `print`.

##### `set`

Takes two arguments, a variable and any other value, and sets the variable to the value.  For example, `set cookies to 10`, `set best_friend to Lewis`, or `set distance to sqrt ((x2-x1)^2 + (y2-y1)^2)`.

##### `shoot`

Creates a Bullet object at the block where the Actor is pointing.  This can be supplied with a different object to shoot, as well as a different direction.

##### `split`

Splits the first argument by using the "glue" or "seperator" given via the second argument.  For example, `split "Time keeps on slippin'" by " "` would give you a list, `["Time", "keeps", "on", "slippin'"]`.

##### `trigger`

Sends an object to a certain label.  An alias of `jump`.

##### `trim`

Trims the first argument, a string, based on the characters in the string in the second argument.  The characters do not have to be in order.  For example, `trim "   Hey!   " of " "` would return `"Hey!"`.


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
