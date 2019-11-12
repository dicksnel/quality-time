import React from 'react';
import { Button, Grid, Header, Icon, Segment } from 'semantic-ui-react';
import { StringInput } from '../fields/StringInput';
import { SubjectType } from './SubjectType';
import { HeaderWithDetails } from '../widgets/HeaderWithDetails';
import { MoveButtonGroup} from '../widgets/MoveButton';
import { ChangeLog } from '../changelog/ChangeLog';
import { delete_subject, set_subject_attribute } from '../api/subject';

export function SubjectTitle(props) {
    const current_subject_type = props.datamodel.subjects[props.subject.type] || { name: "Unknown subject type", description: "No description" };
    const report_uuid = props.report.report_uuid;
    const subject_name = props.subject.name || current_subject_type.name;
    const subject_uuid = props.subject_uuid;
    return (
        <HeaderWithDetails level="h2" header={subject_name} style={{ marginTop: 50 }}>
            <Segment>
                <Header>
                    <Header.Content>
                        {current_subject_type.name}
                        <Header.Subheader>
                            {current_subject_type.description}
                        </Header.Subheader>
                    </Header.Content>
                </Header>
                <Grid stackable>
                    <Grid.Row columns={3}>
                        <Grid.Column>
                            <SubjectType
                                datamodel={props.datamodel}
                                readOnly={props.readOnly}
                                set_value={(value) => set_subject_attribute(report_uuid, subject_uuid, "type", value, props.reload)}
                                subject_type={props.subject.type}
                            />
                        </Grid.Column>
                        <Grid.Column>
                            <StringInput
                                label="Subject name"
                                placeholder={current_subject_type.name}
                                readOnly={props.readOnly}
                                set_value={(value) => set_subject_attribute(report_uuid, subject_uuid, "name", value, props.reload)}
                                value={props.subject.name}
                            />
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column>
                            <ChangeLog
                               report_uuid={report_uuid}
                               subject_uuid={subject_uuid}
                               timestamp={props.report.timestamp}
                            />
                        </Grid.Column>
                    </Grid.Row>
                    {!props.readOnly &&
                        <Grid.Row>
                            <Grid.Column>
                                <MoveButtonGroup
                                    first={props.first_subject}
                                    last={props.last_subject}
                                    moveable="subject"
                                    onClick={(direction) => {
                                        set_subject_attribute(report_uuid, subject_uuid, "position", direction, props.reload)
                                    }}
                                    slot="position"
                                />
                                <Button
                                    basic
                                    floated='right'
                                    negative
                                    icon
                                    onClick={() => delete_subject(report_uuid, subject_uuid, props.reload)}
                                    primary
                                >
                                    <Icon name='trash' /> Delete subject
                                </Button>
                            </Grid.Column>
                        </Grid.Row>
                    }
                </Grid>
            </Segment>
        </HeaderWithDetails>
    )
}
