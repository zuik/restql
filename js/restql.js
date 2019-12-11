import axios from 'axios';

class Query {
    constructor(model) {
        this.model = model;
        this.filterCriteria = undefined;
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
        console.log(url, params);
        const {data} = await axios.get(url, {params: params});

        return data;

    }

    filter(criteria) {
        this.filterCriteria = criteria;
        this.model = `${this.model}/filter`;

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
    const result = await q.filter({"name": {"eq": "ed"}}).all();
    console.log(result);
    result.map((v) => {
        console.log(v.fullname);
    });
}

if (require.main === module) {
    main();
}