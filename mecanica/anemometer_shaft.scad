shaft_height = 100;
shaft_diameter = 12;

insert_diameter = 6;
insert_cut_off =  insert_diameter - 4.5;

insert_cut_off_height = 7;

insert_height = 9;

module insert()
{
    difference(){
        {cylinder(insert_height, d=insert_diameter, $fn=200);}
        translate([-insert_diameter/2, (insert_diameter/2)-insert_cut_off, insert_height-     insert_cut_off_height]) {cube([insert_diameter, insert_cut_off, insert_cut_off_height]);}
     }
 }

module shaft()
{
    difference() {
         {cylinder( shaft_height, d=shaft_diameter, $fn=200);} 
         translate([0,0,-0.1]) {insert();}
     }
}

shaft();