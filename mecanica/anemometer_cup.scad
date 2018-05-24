shaft_insert_height = 4;
cruz_base_height = 10;
arm_height = cruz_base_height - shaft_insert_height;
 
 wall_width = 2;
 
 cup_inner_radius = 20;
 
 module hollow_sphere(){
     difference(){
         {sphere(r=cup_inner_radius + wall_width, $fn=60);}
         {sphere(r=cup_inner_radius, $fn=60);}
         }
     }

module cup(){
    difference() {
        {hollow_sphere();}
        translate([0, 0, -35]) {cube(70, center=true);}
    }
}

cube_total_size = arm_height + wall_width;
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
 
 module cup_with_fix(){
     union(){
         {cup();}
         translate([cup_inner_radius + cube_total_size + 1, 0, cube_total_size/2]) {fix();}
         }
     }
     
  cup_with_fix();