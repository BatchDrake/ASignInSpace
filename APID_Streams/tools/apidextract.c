#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/mman.h>
#include <unistd.h>

struct spp_primary_header {
  union {
    struct {
      uint16_t apid:11;
      uint16_t sec:1;
      uint16_t packet:1;
      uint16_t version:3;
    };

    uint16_t half1;
  };

  union {
    struct {
      uint16_t seq_flags:2;
      uint16_t seq_count:14;
    };

    uint16_t half2;
  };

  uint16_t size;
};

struct spp_timecode_preamble {
  uint8_t fu_size:2;
  uint8_t bu_size:2;
  uint8_t tcid:3;
  uint8_t ext:1;
};

struct spp_timecode_extension {
  uint8_t resv:2;
  uint8_t fu_size:3;
  uint8_t bu_size:2;
  uint8_t ext:1;
};

int
main(int argc, char *argv[])
{
  const uint8_t *data;
  struct spp_primary_header hdr;
  struct stat sbuf;
  int fd;
  uint16_t apid;
  unsigned int p;
  unsigned int i;
  uint16_t size;
  unsigned int sh_size = 0;
  char filename[32];
  
  FILE **apid_fps = NULL;
  
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <input> <secondary_header_size>\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  if (sscanf(argv[2], "%u", &sh_size) < 1) {
    fprintf(stderr, "%s: invalid secondary header size\n", argv[0]);
    exit(EXIT_FAILURE);
  }
  
  if (stat(argv[1], &sbuf) == -1) {
    fprintf(stderr, "%s: cannot stat %s: %s\n", argv[0], argv[1], strerror(errno));
    exit(EXIT_FAILURE);
  }

  apid_fps = calloc(2048, sizeof(FILE *));
  if (apid_fps == NULL) {
    fprintf(stderr, "%s: cannot allocate memory\n", argv[0]);
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

  close(fd);

  p = 0;


  while (p < sbuf.st_size) {
    hdr = *(const struct spp_primary_header *) (data + p);
    p += sizeof(struct spp_primary_header);

    hdr.half1 = ntohs(hdr.half1);
    hdr.half2 = ntohs(hdr.half2);
    hdr.size  = ntohs(hdr.size) + 1;

    apid = hdr.apid;
    if (p + hdr.size > sbuf.st_size)
      break;

    if (apid_fps[apid] == NULL) {
      sprintf(filename, "apid_%04x.bin", apid);
      if ((apid_fps[apid] = fopen(filename, "wb")) == NULL) {
        fprintf(stderr, "%s: failed to open %s: %s\n", argv[0], filename, strerror(errno));
        exit(EXIT_FAILURE);
      }
    }

    
    if (hdr.sec && sh_size <= hdr.size) {
      fwrite(data + p + sh_size, hdr.size - sh_size, 1, apid_fps[apid]);
    } else {
      fwrite(data + p, hdr.size, 1, apid_fps[apid]);
    }
        
    if (apid != 0x7ff) {
      printf("SPP [%04x] -> APID %04x %c (size = %5d) : ", hdr.seq_count, hdr.apid, hdr.sec ? 'S' : '.', hdr.size);

      
      for (i = 0; i < hdr.size; ++i)
        printf("%02x ", data[p + i]);
      printf("\n");
    }

    p += hdr.size;
  }

  return 0;
}
