// Author: Maxime Trépanier
// Date: April 21, 2015

#include "save.hpp"
using namespace std;

static unsigned char col1[3] = {217, 102, 0};  // Orange
static unsigned char col2[3] = {89, 204, 204};  // Blue

//! Save data in a csv file.
void saveData(const margs& args, Ray* output, double maxRadius)
{
    ofstream file;
    double theta, phi;

    file.open(args.name.c_str());
    file << args.x1 << ' ' << args.y1 << ' ' << args.x2 << ' ' << args.y2 << ' ' << args.numX << ' ' << args.numY << endl;
    for (unsigned int i = 0; i < args.numX*args.numY; ++i)
    {
        const Ray& r =  output[i];

        phi = atan2(r.v[1], r.v[0]);  // Spherical coordinates
        theta = acos(r.v[2]);
        file << r.numReflections << ' ' << phi << ' ' << theta;
    }
    file.close();
}

//! Projection onto a spherical color map.
png::image< png::rgb_pixel >& projection(png::image< png::rgb_pixel >& img, const margs& args, Ray* output, double maxRadius)
{
    Ray* ray;
    double theta, phi, a;
    unsigned int r, g, b;

    for (unsigned int i = 0; i < args.numX; ++i)
    {
        for (unsigned int j = 0; j < args.numY; ++j)
        {
            r = g = b = 0;
            a = 1;
            ray = &output[i*args.numY+j];
            phi = atan2(ray->x[1], ray->x[0]);
            theta = acos(ray->x[2]/maxRadius);

            phi = std::cos(phi/2); // Color map, the names of variable are not right (recycling ;) )
            phi *= phi;
            theta = std::sin(theta);
            theta *= theta;
            a = std::exp(-1.*ray->numReflections*args.absorption);

            r = (phi*col1[0] + theta*col2[0])*a;
            g = (phi*col1[1] + theta*col2[1])*a;
            b = (phi*col1[2] + theta*col2[2])*a;

            if (r > 255)  // Saturation
                r = 255;
            if (g > 255)
                g = 255;
            if (b > 255)
                b = 255;

            img[args.numY-j-1][i] = png::rgb_pixel(static_cast<unsigned char>(r), static_cast<unsigned char>(g), static_cast<unsigned char>(b));
        }
    }
    return img;
}
