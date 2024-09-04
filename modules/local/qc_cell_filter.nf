process QC_CELL_FILTER {
    label 'process_medium'

    conda "conda-forge::scanpy conda-forge::python-igraph conda-forge::leidenalg"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/scanpy-scripts:1.9.301--pyhdfd78af_0' :
        'biocontainers/scanpy-scripts:1.9.301--pyhdfd78af_0' }"

    input:
    path(h5ad_raw)
    // path samplesheet

    output:
    path "qc_cell_filter"
    path "qc_cell_filter/*.h5ad",  emit: h5ad_filtered
    path "versions.yml",  emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    """
    qc_cell_filter.py \\
        --h5ad ${h5ad_raw} \\
        --outdir qc_cell_filter \\
        $args \\


    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version | sed 's/Python //g')
    END_VERSIONS        
    """



    // stub:
    // """
    // touch combined_matrix.h5ad
    // """
}