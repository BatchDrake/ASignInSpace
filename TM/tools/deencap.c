#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>

struct tm_primary_header {
  union {
    struct {
      uint16_t ocf:1;
      uint16_t vcid:3;
      uint16_t craftid:10;
      uint16_t vers0ion:2;
    };
    uint16_t first2;
  };
  
  uint8_t mc_count;
  uint8_t vc_count;
  union {
    struct {
      uint16_t pointer:11;
      uint16_t slen:2;
      uint16_t porder:1;
      uint16_t sync:1;
      uint16_t sh_flag:1;
    };
    uint16_t df_status;
  };
} __attribute__ ((packed));

int
main(int argc, char *argv[])
{
  int fd;
  uint8_t prev;
  struct stat sbuf;
  const uint8_t *data;
  unsigned int i, j, p = 0, rows, cols, true_rows = 0;
  unsigned int total;
  unsigned int vcid;
  struct tm_primary_header pm;
  char filename[32];
  int first = 1;
  int recreate = 1;
  int count = 0;
  FILE *enfp = NULL;
  
  size_t datasize;

  
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <input> <vcid>\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  if (sscanf(argv[2], "%u", &vcid) < 1 || vcid >= 8) {
    fprintf(stderr, "%s: invalid VCID\n", argv[0]);
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

  cols = 8920;
  rows = 8 * sbuf.st_size / cols;
  fprintf(stderr, "%d frames\n", rows);

  total = rows * cols / 8;

  p = 0;
  prev = 0;

  for (j = 0; j <  rows; ++j) {
    pm = *(struct tm_primary_header *) (data + (p >> 3));
    pm.first2 = ntohs(pm.first2);
    pm.df_status = ntohs(pm.df_status);

    if (pm.vcid != vcid) {
      p += cols;
      continue;
    }

    if (first) {
      recreate = 1;
      first = 0;
      printf("\033[1;32m(xxx) FIRST FRAME\033[0m\n");
    } else if ((uint8_t) (pm.vc_count - 1) != prev) {
      printf("\033[1;31m(xxx) LOST FRAME\033[0m\n");
      recreate = 1;
    } 

    if (recreate) {
      if (enfp != NULL) {
        fclose(enfp);
      }
      
      sprintf(filename, "encap_%03d.bin", ++count);
      enfp = fopen(filename, "wb");
      if (enfp == NULL) {
        fprintf(stderr, "%s: cannot open %s: %s\n", argv[0], filename, strerror(errno));
        exit(EXIT_FAILURE);
      }

      printf("\033[1mENCAP FILE CREATED: %s\033[0m\n", filename);
    }
    
    printf("(%03x) FRAME %5d [%03x]: ", pm.craftid, pm.mc_count, pm.vc_count);
    if (pm.df_status & 0x8000)
      printf("SECONDARY HEADER!");
    else {
      if (pm.pointer == 2047) {
        printf("(no packet) ");
        pm.pointer = 0;
      } else if (pm.pointer == 2046) {
        printf("(idle data) ");
        pm.pointer = 0;
      }
      
      datasize = cols/8 - 6 - 6 - recreate * pm.pointer;
      printf("%d bytes in the data field", datasize);
      fwrite(data + (p >> 3) + 6 + recreate * pm.pointer, datasize, 1, enfp);
    }
    
    printf("\n");

    prev = pm.vc_count;

    p += cols;
    recreate = 0;
  }
  
  return 0;
}
