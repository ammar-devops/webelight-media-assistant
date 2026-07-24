import { useState } from "react";

function SearchBar({ onSearch }) {
  const [value, setValue] = useState("");

  return (
    <div className="search-box">
      <input
        type="text"
        placeholder="Search Jobs..."
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
          onSearch(e.target.value);
        }}
      />
    </div>
  );
}

export default SearchBar;
