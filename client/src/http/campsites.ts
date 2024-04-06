import { Campsite, CampsiteFilters, CampsiteList } from "models";
import http from "http/http";
import { filterNullValuesFromObject } from "utils/filterNullValues";
import QueryString from "query-string";

export const getCampsites = async (
  page: number,
  limit: number = 25,
  filterState: CampsiteFilters
): Promise<CampsiteList> => {

  const offset = (page - 1) * limit;

  const nonNullFilters =
    filterNullValuesFromObject<CampsiteFilters>(filterState);
  const query = QueryString.stringify(nonNullFilters);
  const results = await http.get<CampsiteList>(
    `/campsites?offset=${offset}&limit=${limit}&${query}`
  );
  return results.data;
};

export const getCampsite = async (campsiteId: string): Promise<Campsite> => {
  const result = await http.get<Campsite>(`/campsites/campsite/${campsiteId}`);
  return result.data;
};
