def get_details():
    return dict(
        name='Account Type Updated',
        description='Account Type Updated based on provided data',
        is_expandable=False,
        is_trigger=True,
        schema=dict(
            type='object',
            additionalProperties=False,
            description='Account Type Updated',
            required=['inputs', 'outputs'],
            properties=dict(
                expand_results=dict(
                    type='boolean',
                    default=False,
                    enum=[False]
                ),
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[],
                    properties=dict()
                ),
                outputs=dict(
                    type='object',
                    required=[
                        'account_type_uuid'
                        'name',
                        "description",
                        'created_ts'
                    ],
                    properties=dict(
                        account_uuid=dict(
                            type='string',
                        ),
                        account_type_uuid=dict(
                            type='string',
                        ),
                        parent_uuids=dict(
                            type='array',
                            items=dict(
                                type='string',
                                format='uuid'
                            )
                        ),
                        name=dict(
                            type='string'
                        ),
                        created_ts=dict(
                            type='integer',
                        )
                    )
                ),
            )
        )
    )


def process(workflow_uuid, account_uuid, node_uuid, trigger_uuid, ingested_ts, processed_ts, inputs, integration,
            **kwargs):
    pass
