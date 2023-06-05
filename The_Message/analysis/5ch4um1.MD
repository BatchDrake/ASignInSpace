# 5ch4um1s interpretation

"What sort of sign? It's hard to explain
because if I say sign to you, you immediately think of a something that can be
distinguished from a something else, but nothing could be distinguished from anything
there"

<img src="../../Candidates/visual/original_square.png" align="center" />

While looking at the different plots of the image that we now call "Starmap" in the Software Hobbits ( https://github.com/Mahlet-Inc/hobbits )
I noticed that the "Hilbert Plot" looked interesting. Not knowing what a Hilbert curve was, 
I consulted a internet search engine and after seeing a few pretty pictures of all sorts of 
space filling curves, I thought it would be a good idea to also check Youtube.
There i found a video by 3Blue1Brown, a very popular maths channel.
I won't link that video here, you should be able to find it easily.
The program he describes of course sounded interesting, so I decided to try and write it in Perl.
As a side note, I'm far from an expert in Perl, or programming for that matter, in fact I started using Perl only a few weeks ago.
But as a side note, its creator Larry Wall, happens to be a linguist, and I'd say you can notice while using it.
Now, back to the curves. That's what they can look like:
<img src="../visual/hilbertcurve.png" align="center" />
(You already knew that because you watched the 3b1b video, that's good.)
I thought it might be a good idea to write different scripts that do one thing each, so I first copied a script that would create the points of the curve,
and then write those points to a text file.
The next script, print.pl, could be used for other things as well, just as a side note.
It takes coordinates as input, and contains the 256x256 starmap image as a hardcoded 2d array.
Give it x and y coordinates, and it tells you if the point is a 0 or a 1.
The (pseudo-)Hilbert curve I created would cross each point in the square.
I wrote these resulting points to another file. Then I wrote (mostly copied together that is) another little Perl script,
which would take  8 bit bitstrings with a "0b" prefix as input, and convert them to decimal, octal, and hexadecimal, and write the binary data to a file.
The resulting image would look as follows:
![junk](https://github.com/5ch4um1/ASignInSpace/assets/36307725/8e51d38c-7a37-44a2-9e78-6e28553b8739)

Visualizing different permutations of the resulting bitmap yielded interesting patterns, all of which would seem to preserve a general structure.
https://github.com/5ch4um1/ASignInSpace/assets/36307725/4256c9c2-f201-4ede-a1ff-311df9392713
And here for comparison the same for the original image data:
https://github.com/5ch4um1/ASignInSpace/assets/36307725/69583f75-3dcd-4452-83f0-f53bd59c98f9
This might demonstrate a further interesting property of space filling curves.

The screenshots that were used to create those videos were created using the following command:
```$ for i in $(seq 256 512); do cat ~/starpoints | xargs -n $i | tr -d " "| tr "0" " "; echo -e "$i\n";sleep 1;scrot -u; done | egrep --color=always  " |1"```
(Keep in mind that this will write a lot of screenshots to your current working directory)
You might "watch them frame by frame" so to say, with the following command:
```for i in $(seq 256 512); do cat ~/starpoints | xargs -n $i | tr -d " "| tr "0" " "; echo -e "$i\n";sleep 1; done | egrep --color=always  " |1" | less -r``` 

My current theories about the meaning do need further research and this document will be updated soon.
