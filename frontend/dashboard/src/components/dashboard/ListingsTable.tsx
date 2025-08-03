
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Eye, Edit } from 'lucide-react';

const listings = [
  {
    id: 1,
    address: "123 Queen Street, Auckland",
    price: "$895,000",
    type: "House",
    bedrooms: 4,
    bathrooms: 2,
    status: "Active",
    daysOnMarket: 12
  },
  {
    id: 2,
    address: "456 Ponsonby Road, Auckland",
    price: "$1,250,000",
    type: "Apartment",
    bedrooms: 2,
    bathrooms: 2,
    status: "Under Offer",
    daysOnMarket: 8
  },
  {
    id: 3,
    address: "789 Remuera Road, Auckland",
    price: "$2,100,000",
    type: "House",
    bedrooms: 5,
    bathrooms: 3,
    status: "Active",
    daysOnMarket: 24
  }
];

export const ListingsTable = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Listings</CardTitle>
        <p className="text-sm text-gray-500">Latest property listings and their status</p>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-600">Property</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Price</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Bed/Bath</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Days on Market</th>
                <th className="text-left py-3 px-4 font-medium text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {listings.map((listing) => (
                <tr key={listing.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <div>
                      <p className="font-medium text-gray-900">{listing.address}</p>
                    </div>
                  </td>
                  <td className="py-3 px-4 font-medium text-green-600">{listing.price}</td>
                  <td className="py-3 px-4 text-gray-600">{listing.type}</td>
                  <td className="py-3 px-4 text-gray-600">{listing.bedrooms}b/{listing.bathrooms}b</td>
                  <td className="py-3 px-4">
                    <Badge variant={listing.status === 'Active' ? 'default' : 'secondary'}>
                      {listing.status}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-gray-600">{listing.daysOnMarket} days</td>
                  <td className="py-3 px-4">
                    <div className="flex space-x-2">
                      <Button variant="ghost" size="sm">
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Edit className="w-4 h-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
};
