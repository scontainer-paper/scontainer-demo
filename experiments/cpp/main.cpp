#include <fstream>
#include <iostream>
#include <iomanip>

#include <nlohmann/json-schema.hpp>

using nlohmann::json;
using nlohmann::json_schema::json_validator;
#define BATCH_NUM 1000000
#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)
// POINT TO THE PATH OF WHERE THE DATASETS ARE LOCATED
#define DATASET_PATH "C:\\Users\\XXXXXXXXX\\CLionProjects\\scontainer-cpp\\datasets"

struct Result {
    double load_time_variable;
    double load_time_fixed;
    double validation_time_variable;
    double validation_time_fixed;
    double validation_time_variable_anyOf;
};

Result run(int batch_size) {
    // load the schema from a file
    // project folder + datasets + A-schema-variable.json
    std::filesystem::path datasetsFolder = std::filesystem::path(DATASET_PATH);
    auto schemaAVariablePath = datasetsFolder / "A-schema-variable.json";
    std::ifstream schemaAVariableFile(schemaAVariablePath);
    auto schemaAFixedPath = datasetsFolder / "A-schema-fixed.json";
    std::ifstream schemaAFixedFile(schemaAFixedPath);
    auto schemaAVariableAnyOfPath = datasetsFolder / "A-schema-variable-anyOf.json";
    std::ifstream schemaAVariableAnyOfFile(schemaAVariableAnyOfPath);

    auto datasetFixedPath = datasetsFolder / ("A-dataset-" + std::to_string(batch_size) + "-fixed.json");
    auto datasetVariablePath = datasetsFolder / ("A-dataset-" + std::to_string(batch_size) + "-variable.json");
    std::ifstream datasetAVariableFile(datasetVariablePath);
    std::ifstream datasetAFixedFile(datasetFixedPath);


    if (!schemaAVariableFile.is_open()) {
        throw std::runtime_error("Failed to open " + schemaAVariablePath.string());
    }
    if (!schemaAFixedFile.is_open()) {
        throw std::runtime_error("Failed to open " + schemaAFixedPath.string());
    }
    if (!schemaAVariableAnyOfFile.is_open()) {
        throw std::runtime_error("Failed to open " + schemaAVariableAnyOfPath.string());
    }
    if (!datasetAVariableFile.is_open()) {
        throw std::runtime_error("Failed to open " + datasetFixedPath.string());
    }
    if (!datasetAFixedFile.is_open()) {
        throw std::runtime_error("Failed to open " + datasetFixedPath.string());
    }


    auto schemaAVariableSchema = json::parse(schemaAVariableFile);
    auto schemaAFixedSchema = json::parse(schemaAFixedFile);
    auto schemaAVariableAnyOfSchema = json::parse(schemaAVariableAnyOfFile);

    json_validator schemaAVariableValidator, schemaAFixedValidator, schemaAVariableAnyOfValidator;
    try {
        schemaAVariableValidator.set_root_schema(schemaAVariableSchema);
        schemaAFixedValidator.set_root_schema(schemaAFixedSchema);
        schemaAVariableAnyOfValidator.set_root_schema(schemaAVariableAnyOfSchema);
    } catch (const std::exception &e) {
        throw std::runtime_error("Failed to validate JSON: " + std::string(e.what()));
    }
    double load_time_variable, load_time_fixed, validation_time_variable, validation_time_fixed,
            validation_time_variable_anyOf;
    auto start = std::chrono::high_resolution_clock::now();
    auto datasetVariable = json::parse(datasetAVariableFile);
    load_time_variable = std::chrono::duration_cast<std::chrono::duration<double> >(
        std::chrono::high_resolution_clock::now() - start).count();
    start = std::chrono::high_resolution_clock::now();
    for (auto &data: datasetVariable) {
        try {
            schemaAVariableValidator.validate(data);
        } catch (const std::exception &e) {
            throw std::runtime_error("Failed to validate JSON: " + std::string(e.what()));
        }
    }
    validation_time_variable = std::chrono::duration_cast<std::chrono::duration<double> >(
        std::chrono::high_resolution_clock::now() - start).count();
    start = std::chrono::high_resolution_clock::now();
    auto datasetFixed = json::parse(datasetAFixedFile);
    load_time_fixed = std::chrono::duration_cast<std::chrono::duration<double> >(
        std::chrono::high_resolution_clock::now() - start).count();
    start = std::chrono::high_resolution_clock::now();
    for (auto &data: datasetFixed) {
        try {
            schemaAFixedValidator.validate(data);
        } catch (const std::exception &e) {
            throw std::runtime_error("Failed to validate JSON: " + std::string(e.what()));
        }
    }
    validation_time_fixed = std::chrono::duration_cast<std::chrono::duration<double> >(
        std::chrono::high_resolution_clock::now() - start).count();
    start = std::chrono::high_resolution_clock::now();

    for (auto &data: datasetVariable) {
        try {
            schemaAVariableAnyOfValidator.validate(data);
        } catch (const std::exception &e) {
            throw std::runtime_error("Failed to validate JSON: " + std::string(e.what()));
        }
    }
    validation_time_variable_anyOf = std::chrono::duration_cast<std::chrono::duration<double> >(
        std::chrono::high_resolution_clock::now() - start).count();
    return {
        load_time_variable,
        load_time_fixed,
        validation_time_variable,
        validation_time_fixed,
        validation_time_variable_anyOf
    };
}


int main() {
    // time the loading of the data
    for (int batch_size: {10000, 50000, 100000, 300000, 500000, 700000, 1000000}) {
        auto result = run(batch_size);
        // tabular results
        // std::cout << std::fixed << std::setprecision(3) << result.load_time_variable << '\t'
        //         << result.load_time_fixed << '\t'
        //         << result.validation_time_variable << '\t'
        //         << result.validation_time_variable_anyOf << '\t'
        //         << result.validation_time_fixed << '\t'
        //         << result.load_time_variable + result.validation_time_variable << '\t'
        //         << result.load_time_variable + result.validation_time_variable_anyOf << '\t'
        //         << result.load_time_fixed + result.validation_time_fixed << std::endl;
        //
        std::cout << "Batch size: " << batch_size << "\n";
        std::cout << "Load time for variable: " << result.load_time_variable << "\n";
        std::cout << "Load time for fixed: " << result.load_time_fixed << "\n";
        std::cout << "Validation time for variable: " << result.validation_time_variable << "\n";
        std::cout << "Validation time for variable anyOf: " << result.validation_time_variable_anyOf << "\n";
        std::cout << "Validation time for fixed: " << result.validation_time_fixed << "\n";
        std::cout << "Load and validation time for variable: " << result.load_time_variable + result.
                validation_time_variable << "\n";
        std::cout << "Load and validation time for variable anyOf: " << result.load_time_variable + result.
                validation_time_variable_anyOf << "\n";
        std::cout << "Load and validation time for fixed: " << result.load_time_fixed + result.validation_time_fixed <<
                "\n";
        std::cout << "----------------------------------------\n";
    }
    return 0;
}
