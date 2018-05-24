shaft_diameter = 12;
vane_head_diameter = 20;

tail_side = 60;
tail_height = 5/sqrt(2);

module tail(){
    union(){
        {cube([tail_side, tail_side, tail_height], center=true);}
        translate([tail_side/2, 0, 0]) {cylinder(tail_height, d=tail_side, center=true);}
        translate([tail_side+vane_head_diameter*1.5/2, 0]) {cube([vane_head_diameter*1.5, tail_height, tail_height], center=true);}
        }
    }
    
 translate([0,0,tail_height/2]) tail();