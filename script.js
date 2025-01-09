const fs = require('fs');

const endpoints = [
    { path: '/categories', methods: ['POST'] },
    { path: '/categories', methods: ['GET'] },
    { path: '/categories/{category_id}', methods: ['PUT'] },
    { path: '/categories/{category_id}', methods: ['DELETE'] },
    { path: '/products', methods: ['POST'] },
    { path: '/products/{product_id}', methods: ['GET'] },
    { path: '/products/{product_id}', methods: ['PUT'] },
    { path: '/products', methods: ['GET'] },
    { path: '/products/{product_id}', methods: ['GET'] },
    { path: '/products/{product_id}', methods: ['DELETE'] },
    { path: '/customers', methods: ['POST'] },
    { path: '/customers', methods: ['GET'] },
    { path: '/customers/{customer_id}', methods: ['GET'] },
    { path: '/customers/{customer_id}', methods: ['PUT'] },
    { path: '/customers/{customer_id}', methods: ['DELETE'] },
    { path: '/orders', methods: ['POST'] },
    { path: '/orders/{order_id}', methods: ['GET'] },
    { path: '/orders/{order_id}', methods: ['DELETE'] },
    { path: '/orders/{order_id}', methods: ['PUT'] },
    { path: '/orders/report/{customer_id}', methods: ['GET'] },
    { path: '/orders/customer/{customer_id}/report', methods: ['GET'] },
];

const generateArtilleryYAML = (endpoints) => {
    const config = {
        config: {
            target: 'http://localhost:8000', // Replace with your base URL
            phases: [
                {
                    duration: 60, // Test duration in seconds
                    arrivalRate: 5, // Virtual users per second
                },
            ],
        },
        scenarios: [],
    };

    endpoints.forEach(({ path, methods }) => {
        methods.forEach((method) => {
            const scenario = {
                flow: [
                    {
                        [method.toLowerCase()]: {
                            url: path,
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            json: method === 'POST' || method === 'PUT' ? {} : undefined, // Include payload for POST/PUT requests
                        },
                    },
                ],
            };
            config.scenarios.push(scenario);
        });
    });

    return config;
};

const saveYAMLToFile = (config, filename) => {
    const yaml = require('js-yaml');
    const yamlString = yaml.dump(config, { noRefs: true });
    fs.writeFileSync(filename, yamlString, 'utf8');
    console.log(`Artillery YAML file has been generated: ${filename}`);
};

const artilleryConfig = generateArtilleryYAML(endpoints);
saveYAMLToFile(artilleryConfig, 'test.yml');
