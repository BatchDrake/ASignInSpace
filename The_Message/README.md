# The Message
It happened. [We managed to extract the message](https://twitter.com/danieladepaulis/status/1664251594064494595). The message can be downloaded [in raw binary form (MSB first)](../Candidates/artifacts/data17.bin) and [plain text bits (ones and zeroes)](../Candidates/artifacts/data17.txt).

A preliminary analysis, including a potential representation as a picture, [can be found here](analysis/preliminary.md).

<p align="center">
  <img src="../Candidates/visual/original_square.png" /><br />
  <sup>Candidate representation of the message, represented as a 256x256 picture.</sup>
</p>

The big question therefore remains: **what does it mean?**

This folder attempts to be a compendium of all the theories on the meaning of the message proposed  by the public in the Discord's channel `#interpretation-chat`.


## Current interpretations
Since the picture representation of the data was the one that raised more interest and may bias the interpretation in the wrong direction, the following list is divided in picture-based and non-picture-based interpretations. **If your interpretation is missing, do not hesitate and send us a pull request with the changes or contact us directly in the Discord channel (HaileyStorm or BatchDrake)**.

### Picture based interpretations
* **[@monarchofshadow's interpretation](analysis/monarchofshadow.md)**
* **[@BatchDrake's analysis on the pattern properties](analysis/batchdrake.md)**
* **[100th aniversary of the birth of Itali Calvino, by @OGIANF](https://discord.com/channels/1066055437457297469/1111404329694400542/1114553195214143561)**
* **[@5ch4um1's Space Filling curves](https://discord.com/channels/1066055437457297469/1111404329694400542/1114292492431528026)**
* **[@OGIANF's Excel Message Map](https://discord.com/channels/1066055437457297469/1111404329694400542/1114164437973205074)** (See also [this message](https://discord.com/channels/1066055437457297469/1111404329694400542/1114553195214143561), and [this](https://discord.com/channels/1066055437457297469/1114553195214143561/1114930547102318662), and [the latest version of the Excel file](https://discord.com/channels/1066055437457297469/1114553195214143561/1114938121147129856))
* **[2D FFT of the cloud as suggested by @kate](https://discord.com/channels/1066055437457297469/1114065866997370900/1114081315533377587)**
* **[Mouse by @BatchDrake](https://discord.com/channels/1066055437457297469/1113919686640406578/1113924669070901420)**
* **[Discussion on other asterisms](https://discord.com/channels/1066055437457297469/1113922788395319456)**

### Non-picture based interpretations
* **[@TheVoroscope's theory on timing sub-structure](https://discord.com/channels/1066055437457297469/1114029303341006849/1114029308286079047)**
* **[Serial protocol by @xenoisx](https://discord.com/channels/1066055437457297469/1115209108245717032)**

### Other
* **[@TheVoroscope's Back to Basics (what's going on?)](https://discord.com/channels/1066055437457297469/1114409536598581298/1114409540360867891)**
* **[@Borna Cesarec's theory of delimiters](https://discord.com/channels/1066055437457297469/1111404329694400542/1114091836181581844)**
* **[Physical constants / keys by mchai](https://discord.com/channels/1066055437457297469/1114030579231494204/1114031417857409044)**
* **[Header / footer analysis by several people](https://discord.com/channels/1066055437457297469/1113883543140044851/1113888584471171194)**

## Unanswered questions
Assuming that the picture is right, [@DareDevil](https://discord.com/channels/1066055437457297469/1114409536598581298/1115281818866950164) made a summary of the currently unanswered questions about the message:

### Regarding "image":
1) Why sparse data? <1% are ON
2) If trying to indicate periodicity or to view as a 256x256 grid, why not just set all the cells that would be on the border ON?
3) Why 5 clusters?
4) Why the 6 "Alignment points" commmon between these?
5) Why are there more APs in some clusters?
6) Why one weird cluster?
7) Why are there few (but not none, or many) points away from clusters?
8) Is it an "image", after all? or is it just a general matrix?

### Regarding data:
1) What could the header and footer possibly help with understanding the image, that they NECESSITATED having a header/footer in the entire signal?
2) Why are they equal in size?

### Regarding the header, specifically:
1) How are you supposed to view the header? 5x16 array or a 8x10 array? (Those are the leading theories now)

### Regarding viewing the header as a 8x10 matrix:
1) Patterns arise: First two bytes are FF, the rest have only 2 bits ON per byte. Why would there be a necessity for it? 
2) Do the first two bytes indicate the dimensions of the body of the data? If so, are the rest just dimensions of something else?
3) Last two bytes alternate, and the first 4 bytes add up to 255.
4) The columns have: 5, 5, 3, 3, 5, 5, 3, 3 number of bits in them respectively. This includes the first two rows. Is this intended? If so, why?
5) The shortened header - (All of it except the first two bytes) - Is this the only configuration in which you can have 2 bits per row to have the given number of column bits, i.e., 3, 3, 1, 1, 3, 3, 1 and 1? If yes, then this is probably a message
