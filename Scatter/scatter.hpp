#ifndef SCATTER_HEAD_INCLUDED
#define SCATTER_HEAD_INCLUDED

// Author: Maxime Trépanier
// Date: April 5, 2015

#include <eigen3/Eigen/Dense>
#include <eigen3/Eigen/Geometry>

#include <vector>

struct SphereOrdering;
const unsigned int d=3;

typedef Eigen::Matrix<double, d, 1> vec;
#define zvec Eigen::ArrayXd::Zero(d)
typedef std::vector<SphereOrdering> vecSO;

const vec s1gr2d(-0.7216878364870322, 1.25, 0);  // Sphere position 2D
const vec s2gr2d(1.4433756729740645, 0, 0);
const vec s3gr2d(-0.7216878364870322, -1.25, 0);
const vec s1gr3d(1, 0, -1/1.4142135623730951);  // Sphere position 3D (rotation needed)
const vec s2gr3d(-1, 0, -1/1.4142135623730951);
const vec s3gr3d(0, 1, 1/1.4142135623730951);
const vec s4gr3d(0, -1, 1/1.4142135623730951);

//! Trajectory
struct Ray
{
    vec x;
    vec v;
    unsigned int numReflections;

    Ray(): numReflections(0)
    {};
    void renormalizeDirection(void);
};

//! Sphere
struct Sphere
{
    vec pos;
    double r;

    Sphere(void): r(0) {};
    Sphere(vec p0, double R): pos(p0), r(R) {};
};

//! Structure to order spheres with sort by their distance
struct SphereOrdering
{
    unsigned int index;
    double distance;

    SphereOrdering(): index(0), distance(0) {};
    SphereOrdering(unsigned int i, double dist): index(i), distance(dist) {};
};

//! Comparison of two SphereOrdering, returns closest.
bool sphereOrderingDistance(const SphereOrdering& s1, const SphereOrdering& s2);

//! Gaspard-Rice-like models
class GRModel
{
public:
    GRModel(double maxR);
    ~GRModel(void) {};

    void addSphere(vec position, double radius);
    void init2D(const double sSpacing, const double sRadius);
    void init3D(const double sSpacing, const double sRadius);

    void orderSphere(vec x0, vecSO& order) const;
    bool iterate(Ray& r) const;

protected:
    std::vector<Sphere> mSphere;
};


#endif // SCATTER_HEAD_INCLUDED
