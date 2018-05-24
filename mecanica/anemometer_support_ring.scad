shaft_diameter = 12;



shaft_insert_height = 4;
cruz_base_height = 10;
wall_width = 2;
arm_height = cruz_base_height - shaft_insert_height;
cube_total_size = arm_height + wall_width;

support_ring_height = arm_height;
support_ring_radius = 20;

module ring()
{
    difference() {
        {cylinder(support_ring_height, r=support_ring_radius, $fn=60);}
        {cylinder(support_ring_height*1.2, d=shaft_diameter*1.1, $fn=60);}
     }
}

module hollow_cube(){
    difference(){
        {cube([cube_total_size*2, cube_total_size, cube_total_size], center=true);}
        {cube([arm_height*2, arm_height, arm_height], center=true);}
        }
    }

module fix(){
    difference() {
        difference(){
            {hollow_cube();}
            translate([0, 0, arm_height]) {cube(([cube_total_size*2, cube_total_size, cube_total_size]), center=true);}
            }
        translate([arm_height*2, 0, 0]) {cube(([cube_total_size*2, cube_total_size, cube_total_size]), center=true);}
    }
 }
 
module support_ring(){
    union(){
        {ring();}
        rotate([0, 0, 0]) {translate([arm_height + support_ring_radius, 0, cube_total_size/2]) {fix();}}
        rotate([0, 0, 120]) {translate([arm_height + support_ring_radius, 0, cube_total_size/2]) {fix();}}
        rotate([0, 0, 2400]) {translate([arm_height + support_ring_radius, 0, cube_total_size/2]) {fix();}}
        }
    }

support_ring();