function TodoFilters({ filters, onChange, onSubmit }) {
    const updateFilter = event => {
        const { name, value } = event.target;
        onChange({ ...filters, [name]: value, page: 1 });
    };

    return (
        <section className="panel filter-panel">
            <form className="filter-form" onSubmit={onSubmit}>
                <div className="field-group search-field">
                    <label htmlFor="keyword">Tìm kiếm</label>
                    <input
                        id="keyword"
                        type="search"
                        name="keyword"
                        value={filters.keyword}
                        placeholder="Nhập tiêu đề hoặc mô tả"
                        onChange={updateFilter}
                    />
                </div>

                <div className="field-group">
                    <label htmlFor="status">Trạng thái</label>
                    <select id="status" name="status" value={filters.status} onChange={updateFilter}>
                        <option value="all">Tất cả</option>
                        <option value="active">Chưa xong</option>
                        <option value="completed">Hoàn thành</option>
                    </select>
                </div>

                <div className="field-group">
                    <label htmlFor="sort">Sắp xếp</label>
                    <select id="sort" name="sort" value={filters.sort} onChange={updateFilter}>
                        <option value="newest">Mới nhất</option>
                        <option value="oldest">Cũ nhất</option>
                        <option value="title">A-Z</option>
                        <option value="status">Trạng thái</option>
                    </select>
                </div>

                <button className="btn btn-dark" type="submit">Lọc</button>
            </form>
        </section>
    );
}

export default TodoFilters;
