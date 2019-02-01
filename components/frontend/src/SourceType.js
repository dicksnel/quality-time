import React, { Component } from 'react';
import { Dropdown } from 'semantic-ui-react';

class SourceType extends Component {
  constructor(props) {
    super(props);
    this.state = { edit: false, hover: false }
  }
  onMouseEnter(event) {
    this.setState({ hover: true })
  }
  onMouseLeave(event) {
    this.setState({ hover: false })
  }
  onEdit() {
    this.setState({ edit: true });
  }
  onClose() {
    this.setState({ edit: false });
  }
  onKeyDown(event) {
    if (event.key === "Escape") {
      this.setState({ edit: false });
      this.props.reset_source_type();
    }
  }
  onSubmit(event, { name, value }) {
    event.preventDefault();
    this.setState({ edit: false })
    this.props.post_source_type(value);
  }
  render() {
    let options = [];
    let self = this;
    this.props.datamodel["metrics"][this.props.metric_type]["sources"].forEach(
      (key) => { options.push({ text: self.props.datamodel["sources"][key]["name"], value: key }) });
    if (this.state.edit) {
      return (
        <Dropdown fluid selectOnNavigation={false} defaultOpen value={this.props.source_type}
          options={options} onChange={(e, { name, value }) => this.onSubmit(e, { name, value })} tabIndex="0" />
      )
    }
    const style = this.state.hover ? { borderBottom: "1px dotted #000000" } : { height: "1em" };
    return (
      <div onClick={(e) => this.onEdit(e)} onKeyPress={(e) => this.onEdit(e)}
        onMouseEnter={(e) => this.onMouseEnter(e)} onMouseLeave={(e) => this.onMouseLeave(e)} style={style} tabIndex="0">
        {this.props.datamodel["sources"][this.props.source_type]["name"]}
      </div>
    )
  }
}

export { SourceType };
