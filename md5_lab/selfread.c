#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    FILE *fp = fopen(argv[0], "rb");
    if (!fp) {
        printf("Cannot open self\n");
        return 1;
    }
    
    // Seek to a specific offset where collision data is stored
    fseek(fp, 12352, SEEK_SET);
    
    unsigned char data[128];
    fread(data, 1, 128, fp);
    fclose(fp);
    
    printf("Collision block data:\n");
    for (int i = 0; i < 128; i++) {
        printf("%02x", data[i]);
        if ((i+1) % 32 == 0) printf("\n");
    }
    printf("\n");
    
    return 0;
}
