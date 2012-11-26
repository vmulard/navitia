#include "get_stop_times.h"
#include "routing/best_trip.h"
#include "type/pb_converter.h"
namespace navitia { namespace timetables {

std::string iso_string(const nt::Data & d, int date, int hour){
    boost::posix_time::ptime date_time(d.meta.production_date.begin() + boost::gregorian::days(date));
    date_time += boost::posix_time::seconds(hour);
    return boost::posix_time::to_iso_string(date_time);
}



std::vector<dt_st> get_stop_times(const std::vector<type::idx_t> &route_points, const routing::DateTime &dt, const routing::DateTime &max_dt, const int nb_departures, type::Data & data) {
   std::vector<dt_st> result;
   std::multiset<dt_st, comp_st> result_temp;
   auto test_add = true;
   auto last_departure = dt;
   std::vector<type::idx_t> rps = route_points; //On veut connaitre poru tous les route points leur premier départ

   while(test_add && last_departure < max_dt &&
         (distance(result_temp.begin(), result_temp.upper_bound(std::make_pair(last_departure, type::invalid_idx))) < nb_departures)) {

       test_add = false;
       //On va chercher le prochain départ >= last_departure + 1 pour tous les route points de la liste
       for(auto rp_idx : rps) {
           const type::RoutePoint & rp = data.pt_data.route_points[rp_idx];
           auto etemp = earliest_trip(data.pt_data.routes[rp.route_idx], rp.order, last_departure + 1, data);
           if(etemp >= 0) {
               auto st = data.pt_data.stop_times[data.pt_data.vehicle_journeys[etemp].stop_time_list[rp.order]];
               auto dt_temp = dt;
               dt_temp.update(st.departure_time);
               result_temp.insert(std::make_pair(dt_temp, st.idx));
               test_add = true;
           }
       }

       //Le prochain départ sera le premier dt >= last_departure
       last_departure = result_temp.upper_bound(std::make_pair(last_departure, type::invalid_idx))->first;
       //On met à jour la liste des routepoints à updater (ceux qui sont >= last_departure
       rps.clear();
       for(auto it_st = result_temp.lower_bound(std::make_pair(last_departure, type::invalid_idx));
                it_st!= result_temp.upper_bound(std::make_pair(last_departure, type::invalid_idx)); ++it_st){
           rps.push_back(data.pt_data.stop_times[it_st->second].route_point_idx);
       }

   }

   int i = 0;
   for(auto it = result_temp.begin(); it != result_temp.end() && i < nb_departures; ++it) {
       if(it->first <= max_dt) {
           result.push_back(*it);
       } else {
           break;
       }
       ++i;
   }

   return result;
}


}

}