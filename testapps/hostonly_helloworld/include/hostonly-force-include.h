/*
 * What is this?
 *
 * This is a solution to nastly long command lines
 * 
 * Often an IDE has a small window to list command line defines.
 * This small windows is too small to edit and add things to.
 *
 * I first came across these with the older 68k Mac compiler
 * There was "jam file" that you could jam infront of all other
 * files the compiler reads.
 *
 * What is great about this file is as follows:
 *  1) It can be huge - instead of that small window.
 *  2) It can contain comments like this.
 *  3) You can have hundreds of #defines
 *
 *=================
 * The rules that I follow:
 *  a) This file technically is a C file
 *     so you can do lots of other stuff
 *     Like define typedefs, structs and
 *     you can include other files.
 *
 *  b) I do not, I only have #defines nothing else.
 */

/* For this simple example it is a simple file
 * with nothing in the file, it is for demonstration only.
 */

