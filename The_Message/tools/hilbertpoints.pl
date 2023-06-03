#!/bin/perl

#This script will output the points of a space filling curve to stdout.
#For more information, see also: https://metacpan.org/pod/Math::PlanePath::HilbertCurve
#usage: ./hilbertpoints.pl
use Math::PlanePath::HilbertCurve;

my $path = Math::PlanePath::HilbertCurve->new;
my @a = (0..65535);
my $i = 0;
for $i(@a){
my($x, $y) = $path->n_to_xy($i);
print "$x $y\n"
}
