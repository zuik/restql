import axios from 'axios';

class Query {
    constructor(model) {
        this.model = model;
    }

    async all() {
        // GET model/all
        console.log(`GET ${this.model}/all`);
        const url = `${this.model}/all`;

        const r = await axios.get(url);
        if (r.data) {
            return r.data;
        } else {
            return null;
        }

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
    let result = await q.all();

    console.log(result);
}

if (require.main === module) {
    main();
}