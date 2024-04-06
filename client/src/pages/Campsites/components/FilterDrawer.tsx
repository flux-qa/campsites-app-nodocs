import React from "react";
import { Button, Drawer, Divider } from "@mantine/core";
import { CampsiteFilters } from "models";
import { Filters } from ".";
import { defaultFilterState } from "constants/defaultFilterState";
import { useElementSize } from "@mantine/hooks";

type FilterDrawerProps = {
  filterState: CampsiteFilters;
  handleFilterStateChange: (val: CampsiteFilters) => void;
  handleClearFilters: () => void;
  numResults: number | undefined;
  open: boolean;
  setClosed: () => void;
};

const FilterDrawer = (props: FilterDrawerProps): JSX.Element => {

  const { ref: totalRef, height: totalHeight } = useElementSize();
  const { ref: headerRef, height: headerHeight } = useElementSize();
  const { ref: footerRef, height: footerHeight } = useElementSize();


  const filtersHeight = totalHeight - headerHeight - footerHeight - 48;

  const resetFiltersDisabled =
    JSON.stringify(props.filterState) === JSON.stringify(defaultFilterState);

  return (
    <Drawer.Root
      opened={props.open}
      onClose={props.setClosed}
      position="right"
      keepMounted
    >
      <Drawer.Overlay />
      <Drawer.Content ref={totalRef} maw="calc(100vw - 10%)">
        <Drawer.Header ref={headerRef} sx={{ zIndex: 2000 }}>
          <Drawer.Title sx={{ fontSize: 22, fontWeight: 600 }}>
            Filters
          </Drawer.Title>
          <Drawer.CloseButton />
        </Drawer.Header>
        <Drawer.Body
          style={{
            maxHeight: filtersHeight,
          }}
        >
          <div>
            <Filters
              filterState={props.filterState}
              handleFilterStateChange={props.handleFilterStateChange}
            />
          </div>
        </Drawer.Body>
        <div
          ref={footerRef}
          style={{
            width: "100%",
            textAlign: "center",
            padding: "0px 16px 16px 16px",
            position: "fixed",
            bottom: 0,
            backgroundColor: "white",
            zIndex: 2000,
          }}
        >
          <Divider
            my="sm"
            labelPosition="center"
            label={
              props.numResults !== undefined
                ? `${props.numResults} results`
                : "Loading..."
            }
          />
          <Button
            variant="outline"
            disabled={resetFiltersDisabled}
            onClick={props.handleClearFilters}
            w="100%"
          >
            Clear Filters
          </Button>
        </div>
      </Drawer.Content>
    </Drawer.Root>
  );
};

export default FilterDrawer;
