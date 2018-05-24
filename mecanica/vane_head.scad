shaft_diameter = 12;
vane_head_diameter = 20;

tail_side = 60;
tail_height = 5/sqrt(2);

module head(){
    difference(){
        {cylinder(30, r1=10, r2=0.5, $fn=60);}
        {cube([tail_height*1.1, tail_height*1.1, 5], center=true);}
    }
    }
    
 head();