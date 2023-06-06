#!/bin/perl

#This script takes a 8 bit binary string (that is, 0s and 1s as text) with a "0b" prefix as input, 
#and outputs the original input, and its decimal, octal, and hexadecimal values to stdout.
#It also writes the input as binary to the file output.data
#example usage:
#   $ echo -e "0b10101010\n0b01010101" | ./convert.pl
#    0b10101010 170 252 AA
#    0b01010101 85 125 55
#   $ xxd output.data 
#   00000000: aa55                                     .U
#
#You may use e.g. awk for adding the "0b" if your strings don't have that prefix yet.
use strict;
use warnings;
open( FH, ">output.data" ) or die "dang it!\n";

foreach my $line ( <STDIN> ){
chomp $line; 
my $decvalue = oct($line);
my $octvalue = sprintf("%o", $decvalue);
my $hexvalue = sprintf("%X", $decvalue);
my $binary = pack ('W*', $decvalue);
print "$line $decvalue $octvalue $hexvalue\n";
syswrite ( FH, $binary );
}
close FH;
