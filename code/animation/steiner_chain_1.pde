

void setup(){
  size(600,600);
  
  strokeWeight(1);
  noFill();
  loop();
  
}


float r1 = 75;

float m = 1;
float n = 7;
float alpha = m * PI / n;

float r2 = r1 * pow(tan(alpha)  + (1/cos(alpha)), 2);


void draw(){
  
  //background(255);
  
  float x1 = width/2, y1 = height/2;
  float x2 = width/2, y2 = height/2;
  
  x1 = 0.55 * width;
  y1 = 0.6*height;

  f(x1, y1, r1, x2, y2, r2);

}


float steiner_ang = 0.0;
float steiner_inc = 2*PI/n;

void f(float x1, float y1, float r1, float x2, float y2, float r2){
  
  ellipse(x1, y1, 2*r1, 2*r1);
  ellipse(x2, y2, 2*r2, 2*r2);
  
  
  // Ellipse on which centres of steiner chain lie.
  
  // major axis
  float a = r1 + r2;
  // eccentricity related to distance between centres.
  float p = dist(x1, y1, x2, y2);
  // minor axis
  float b = sqrt(a*a - p*p);
  // angle of inclination
  float t = atan2(y2-y1, x2-x1);
  // ellipse centre.
  float ex = 0.5*(x1+x2);
  float ey = 0.5*(y1+y2);

  ellipse_3(a, b, ex,ey, t);
  
  
  float xy[];
  xy = ellipse_pt(a, b, ex, ey, t, steiner_ang);
  
  float d = 2* (dist(xy[0], xy[1], x1, y1) - r1); //<>//
  
  ellipse(xy[0], xy[1], d, d);
  ellipse(xy[0], xy[1], 10, 10);
  
  steiner_ang += steiner_inc;
  
  if (frameCount > n){
    noLoop();
  }
  
}

float [] ellipse_pt(float axis1, float axis2, float xCent, float yCent, float ang, float theta){
 
  float ct = cos(theta);
  float st = sin(theta);

  float ca = cos(ang);
  float sa = sin(ang);
  
  float px = 0.5 * axis1 * ct;
  float py = 0.5 * axis2 * st;
  
  float px2 = ca * px - sa * py;
  float py2 = sa * px + ca * py;
  
  px2 += xCent;
  py2 += yCent;
  
  float xy[] = {px2, py2};
  
  return xy;
}

void ellipse_3(float axis1, float axis2, float x, float y, float ang){
  // Ellipse with given axes and centre at a given angle ...
  
  pushMatrix();
  
  translate(x, y);
  rotate(ang);
     //<>//
  pushStyle();
  stroke(255,0,0,128);
  ellipse(0, 0, axis1, axis2);
  popStyle();  

  popMatrix();
}