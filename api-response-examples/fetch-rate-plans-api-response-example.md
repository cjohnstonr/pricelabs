# Fetch Rate Plans API Response Example

Generated: 2025-09-16T16:45:00.000000

## Response Structure

```json
{
  "rate_plans": {
    "id": "4305303",
    "pms": "airbnb",
    "name": "Chic 1BR in Trendy Walkable South Park",
    "rateplans": {}
  }
}
```

## Notes

This is the actual API response for a sync-enabled listing (ID: 4305303). The `rateplans` object is empty, which appears to be the standard response for Airbnb listings. 

According to the API documentation, rate plans are used to fetch adjustments for non-default rate plans, which may not be applicable to standard Airbnb listings. The endpoint returns:
- `id`: The listing ID
- `pms`: The property management system
- `name`: The property name
- `rateplans`: An object that would contain rate plan adjustments if available

For listings that do have rate plans, the structure would include rate plan IDs with adjustment details like type, default status, and percentage/fixed adjustments.