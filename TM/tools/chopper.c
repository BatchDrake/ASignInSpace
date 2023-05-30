#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>

#define WIDTH 8920

int
main(int argc, char *argv[])
{
  int fd;
  struct stat sbuf;
  const uint8_t *data;
  unsigned int i, j, p = 0, rows, cols;
  unsigned int total;
  
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <input>\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  if (stat(argv[1], &sbuf) == -1) {
    fprintf(stderr, "%s: cannot stat %s: %s\n", argv[0], argv[1], strerror(errno));
    exit(EXIT_FAILURE);
  }

  if ((fd = open(argv[1], O_RDONLY)) == -1) {
    fprintf(stderr, "%s: cannot open %s: %s\n", argv[0], argv[1], strerror(errno));
    exit(EXIT_FAILURE);
  }

  data = mmap(NULL, sbuf.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (data == (const uint8_t *) -1) {
    fprintf(stderr, "%s: mmap failed: %s\n", argv[0], argv[1]);
    exit(EXIT_FAILURE);
  }

  cols = WIDTH;
  rows = 8 * sbuf.st_size / cols;
  fprintf(stderr, "Total: %d blocks\n", rows);

  total = rows * cols / 8;

  printf("P1\n");
  printf("%d %d\n", cols, rows);
 
  for (j = 0; j <  rows; ++j) {
    for (i = 0; i < cols; ++i) {
      putchar((data[p >> 3] & (1 << (7 - (p & 7)))) ? '1' : '0');
      putchar(32);
      ++p;
    }
    putchar(10);
  }
  
  return 0;
}
