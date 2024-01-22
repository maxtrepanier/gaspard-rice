// Author: Maxime Trépanier
// Date: April 5, 2015

#include <cmath>
#include <vector>
#include "scatter.hpp"

bool sphereOrderingDistance(const SphereOrdering& s1, const SphereOrdering& s2)
{
    return s1.distance < s2.distance;
}

void Ray::renormalizeDirection(void)
{
    v /= v.norm();
}

GRModel::GRModel(double maxR)
{
    mSphere.push_back(Sphere(zvec, maxR));
}

void GRModel::addSphere(vec position, double radius)
{
    mSphere.push_back(Sphere(position, radius));
}

//! Add spheres for GR2D model.
void GRModel::init2D(const double sSpacing, const double sRadius)
{
    addSphere(s1gr2d*sSpacing, sRadius);
    addSphere(s2gr2d*sSpacing, sRadius);
    addSphere(s3gr2d*sSpacing, sRadius);
}

//! Add spheres for GR3D model.
void GRModel::init3D(const double sSpacing, const double sRadius)
{
    Eigen::Matrix3d O = Eigen::AngleAxisd(-M_PI_4, Eigen::Vector3d::UnitY()).toRotationMatrix();

    addSphere(O*s1gr3d*sSpacing, sRadius);
    addSphere(O*s2gr3d*sSpacing, sRadius);
    addSphere(O*s3gr3d*sSpacing, sRadius);
    addSphere(O*s4gr3d*sSpacing, sRadius);
}

void GRModel::orderSphere(vec x0, vecSO& order) const
{
    vec v;
    order.resize(mSphere.size());

    for (size_t i = 1; i < mSphere.size(); ++i)
    {
        v = mSphere[i].pos - x0;
        order[i-1] = SphereOrdering(i, v.norm());  // Add the sphere index and its distance to the vector
    }
    sort(order.begin(), order.end()-1, sphereOrderingDistance);  // Sort the vector by increasing distance
    order[mSphere.size()-1] = SphereOrdering(0, x0.norm());  // Add outer sphere
}

bool GRModel::iterate(Ray& r) const
{
    vecSO order;
    orderSphere(r.x, order);
    vec n, tmp, tmp2;
    double vd = 0, delta = 0;

    for (vecSO::iterator it = order.begin(); it != order.end(); ++it)
    {
        const Sphere& s = mSphere[it->index];
        const double& l = it->distance;
        tmp = s.pos - r.x;  // vector l
        vd = r.v.dot(tmp);
        delta = s.r*s.r + vd*vd - l*l;  // delta^2

        if (delta < 0 || (vd < 0 && it->index != 0))  // Collision?
            continue;  // If not, go to next sphere

        delta = -std::sqrt(delta);
        if (s.r > l)
            delta *= -1;

        r.numReflections++;
        r.x = r.x + (vd + delta)*r.v;  // New position
        n = (r.x - s.pos);  // Vector normal to the surface of the sphere

        if (it->index == 0)  // If the impact is on the outer sphere, we stop iterating
            return false;

        r.v = r.v - 2*n.dot(r.v)/s.r*n;  // else, compute the new v_i
        return true;
    }
    return false;  // In any case... should not come to this.
}
