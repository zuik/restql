import axios from 'axios';

class Query {
    constructor(model) {
        this.model = model;
        this.filterCriteria = undefined;
        this.orderByCriteria = undefined;
        this.joinCriteria = undefined;
    }

    async all() {
        const url = `${this.model}`;
        // Right now we only support all() to finalize the query.
        let params = {
            "finalize": "all"
        };
        if (this.filterCriteria) {
            params["filter"] = this.filterCriteria;
        }
        if (this.orderByCriteria) {
            params["orderBy"] = this.orderByCriteria;
        }
        if (this.joinCriteria) {
            params["join"] = this.joinCriteria;
        }
        console.log(url, params);
        const {data} = await axios.get(url, {params: params});

        return data;

    }

    /**
     * Filter the query.
     *
     * @param criteria - Criteria for filtering the query. We accept the criteria in the form of {property name: {operator: value} }. Current supported operator are: "eq" -> "==",
     * @returns {Query}
     */
    filter(criteria) {
        this.filterCriteria = criteria;
        this.model = `${this.model}/filter`;

        return this;
    }

    orderBy(criteria) {
        this.orderByCriteria = criteria;
        this.model = `${this.model}/orderBy`;

        return this;
    }

    join(criteria) {
        this.joinCriteria = criteria;
        this.model = `${this.model}/join`;

        return this;
    }
}

/**
 * Make a Query
 * @param model : URL to the model
 */
function query(model) {
    return new Query(model)
}

async function main() {
    let q = new Query("http://localhost:5000/users");
    // const result = await q.all();
    // const result = await q.filter({"name": {"eq": "ed"}}).all();
    // const result = await q.orderBy({"name": {"asc": true}}).all();
    // const result = await q.join({"id": {"filter": "user_id"}}).all();
    const result = await q.join().all();
    console.log(result);
    result.map((v) => {
        console.log(v.fullname);
    });
}

if (require.main === module) {
    main();
}