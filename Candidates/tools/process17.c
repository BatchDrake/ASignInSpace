#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <stdint.h>
#include <stdbool.h>

#define read_or_exit(what, size) if (fread(&what, size, 1, stdin) < 1) exit(0)

int
main(void)
{
  uint8_t type;
  uint32_t offset, size;
  char data[8];
  uint32_t trailer;
  
  for (;;) {
    read_or_exit(type, 1);
    read_or_exit(offset, 4);
    offset = ntohl(offset);

    read_or_exit(size, 4);
    size = ntohl(size);
                 
    read_or_exit(data, size);
    read_or_exit(trailer, 4);


    fwrite(data, size, 1, stdout);
  }
  
  return 0;
}


