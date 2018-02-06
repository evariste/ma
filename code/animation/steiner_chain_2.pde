float m = 1; // Fixed !!

int n = 7;
float alpha = m * PI / float(n);

// Outer:
float r2 = 1.0;
// Inner:
float r1 = r2 / pow(tan(alpha)  + (1/cos(alpha)), 2);
// Half way between
float rmid = 0.5 * (r1 + r2);

// Inner:
float []cInner = {0, 0, 2*r1};
// Outer
float []cOuter = {0, 0, 2*r2};

// Main chain.
float [][]ck = new float[n][3];

// Secondary inners
float [][]c1_2 = new float[n][3];
// Secondary chains
float [][][]ck_2 = new float[n][n][3];


float [] inv_pt = new float[2];
float inv_rad;
float inv_rad_sq;

float scale_fac;
float phase = 0.0;
float phase_inc = 0.005;

PVector vec1;

void setup(){
  size(600,600);
  strokeWeight(1);
  noFill();

  scale_fac = 0.4*0.5*(height + width);
  
  update_inv_rad();
  
  loop();
}


void draw(){
  int k,j;
  float [] c_inv = new float[3];
  
  background(220);
  
  setup_chain();
  phase += phase_inc;
  
  inv_pt[0] = 3.2 * sin(phase+PI/2);
  inv_pt[1] = 1.2;
  update_inv_rad();
  

  pushStyle();
  stroke(255,255,255);
  strokeWeight(2);
  fill(20, 200, 100, 30);
  draw_circ(cOuter);
  popStyle();
  
  color inner_col = color(200, 50, 155, 230);
  
  invert_circle(cInner, c_inv);
  //stroke(0,255,0);
  pushStyle();
  fill(inner_col);
  draw_circ(c_inv);
  popStyle();
  
  for (k=0; k < n; k++){
  }
  

  stroke(0);
  for (k=0; k < n; k++){
    fill(150,100,0,100);
    invert_circle(ck[k], c_inv);
    //fill(255,255,255);
    draw_circ(c_inv);

    invert_circle(c1_2[k], c_inv);
    pushStyle();
    fill(inner_col);
    draw_circ(c_inv);
    popStyle();

    for (j=0; j < n; j++){
      invert_circle(ck_2[k][j], c_inv);
      pushStyle();
      fill(get_colour(j));
      draw_circ(c_inv);
      popStyle();
    }
  }
  

  if (phase < 2*PI){
   saveFrame("frames/f####.png");
  }
  
  float xy[] = new float[3];
  
  boolean draw_inverter = false;
  
  if (draw_inverter){
    xy[0] = inv_pt[0];
    xy[1] = inv_pt[1];
    xy[2] = 2*inv_rad;
    draw_circ(xy);
  }

}

float [] invert_pt(float []xy){
  
  float d1 = dist(xy[0], xy[1], inv_pt[0], inv_pt[1]);
  float d2 = inv_rad_sq / d1;
  xy[0] = inv_pt[0] + d2 * (xy[0] - inv_pt[0]) / d1;
  xy[1] = inv_pt[1] + d2 * (xy[1] - inv_pt[1]) / d1;
  return xy;
}

void invert_circle(float []circ, float[] circ_out){
  
  PVector v = new PVector(circ[0] - inv_pt[0], circ[1] -  inv_pt[1]);
  PVector u = v.div(v.mag());
  
  float [] pA = new float[2];
  float [] pB = new float[2];
  float r = circ[2] / 2.0;
  
  pA[0] = circ[0] + r * u.x;
  pA[1] = circ[1] + r * u.y;
  
  pB[0] = circ[0] - r * u.x;
  pB[1] = circ[1] - r * u.y;
  
  pA = invert_pt(pA);
  pB = invert_pt(pB);
    
  circ_out[0] = 0.5 * (pA[0] + pB[0]);
  circ_out[1] = 0.5 * (pA[1] + pB[1]);
  circ_out[2] = dist(pA[0], pA[1], pB[0], pB[1]);
  
}


void draw_circ(float []circ){
  // Take a circle scaled for the unit disk and plot in the window.
  ellipse(scale_fac*circ[0] + width/2, scale_fac*circ[1] + height/2, circ[2]*scale_fac, circ[2]*scale_fac);
}

void setup_chain(){
  float t;
  int k;
  int j;
  
  for (k=0; k < n; k++){
    t = phase + k * 2.0 * PI / n;
    ck[k][0] = rmid * cos(t);
    ck[k][1] = rmid * sin(t);
    ck[k][2] = r2-r1;
    
    c1_2[k][0] = ck[k][0];
    c1_2[k][1] = ck[k][1];
    c1_2[k][2] = r1 * ck[k][2]; 
  }
  
  float cent_j_x, cent_j_y, d_j;
  
  for(j = 0; j < n; j++){
    
    cent_j_x = ck[j][0];
    cent_j_y = ck[j][1];
    d_j = ck[j][2];
    
    for(k = 0; k < n; k++){
      t = -3.0 * (phase + k * 2.0 * PI / n);

      // d_new / d_j = d_j / 2
      // x_new = cent_j_x + cent_k_x * (d_j / 2) = 
      // y_new = cent_y + cent_y * (dj /2)

      //ck_2[j][k][0] = cent_j_x + ck[k][0] * (d_j / 2);
      //ck_2[j][k][1] = cent_j_y + ck[k][1] * (d_j / 2);

      ck_2[j][k][0] = cent_j_x + rmid * cos(t) * (d_j / 2);
      ck_2[j][k][1] = cent_j_y + rmid * sin(t) * (d_j / 2);
      
      ck_2[j][k][2] = d_j * d_j / 2;
    }
    
  }
  
}

void update_inv_rad(){
  float inv_pt_O = dist(inv_pt[0], inv_pt[1], 0, 0);
  inv_rad = sqrt(inv_pt_O*inv_pt_O - 1);
  inv_rad_sq = inv_rad * inv_rad;
 
}

color get_colour(int k){
  
  float kk = k;

  if (kk > n/2){ //<>//
    kk = n - kk;
  }
  
  kk = kk * 2 / n;
  
  float r = kk * 5 + (1-kk)*70;
  float g = kk * 80 + (1-kk) * 10;
  float b = kk * 100 + (1-kk) * 200;
  return color(r, g, b, 255);
}